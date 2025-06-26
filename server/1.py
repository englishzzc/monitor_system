#!/usr/bin/env python3
import psutil
import time
import os
import json
import mmap
import ctypes
import posix_ipc
import signal
import sys
import asyncio
import websockets
# import redis
from datetime import datetime
from typing import Dict, Any

# ------------------- 配置参数 -------------------
CONFIG = {
    "采集间隔": 0.2,  # 单位：秒
    "共享内存路径": "/sysmon_shm",
    "信号量名称": "/sysmon_sem",
    "WebSocket端口": 8765,
    "Redis服务器": "localhost",
    "Redis通道": "system_stats",
}


# ------------------- 数据结构定义 -------------------
class SystemStats(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("timestamp", ctypes.c_double),
        ("cpu_percent", ctypes.c_float),
        ("mem_total", ctypes.c_uint64),
        ("mem_used", ctypes.c_uint64),
        ("net_sent", ctypes.c_uint64),
        ("net_recv", ctypes.c_uint64),
        ("disk_usage", ctypes.c_float),
    ]


# ------------------- 数据采集器 -------------------
class SystemMonitor:
    def __init__(self):
        self._running = True
        self._prev_net = psutil.net_io_counters()

        # 初始化共享内存
        self.shm = posix_ipc.SharedMemory(
            CONFIG["共享内存路径"],
            flags=posix_ipc.O_CREAT,
            size=ctypes.sizeof(SystemStats),
        )
        self.buffer = mmap.mmap(self.shm.fd, self.shm.size)
        self.sem = posix_ipc.Semaphore(CONFIG["信号量名称"], flags=posix_ipc.O_CREAT, mode=0o666, initial_value=1)
        os.chmod("/dev/shm/sem.sysmon_sem", 0o666)
        print("信号量:",self.sem)

        # 初始化Redis
        # self.redis = redis.Redis(host=CONFIG["Redis服务器"], decode_responses=True)

    def _collect_data(self) -> Dict[str, Any]:
        """采集系统指标并计算差值"""
        net = psutil.net_io_counters()
        delta = {
            "net_sent": net.bytes_sent - self._prev_net.bytes_sent,
            "net_recv": net.bytes_recv - self._prev_net.bytes_recv,
        }
        self._prev_net = net
        # print("timestamp", time.time())
        # print("cpu_percent", psutil.cpu_percent())
        # print("memory", psutil.virtual_memory())

        return {
            "timestamp": time.time(),
            "cpu_percent": psutil.cpu_percent(),
            "memory": psutil.virtual_memory(),
            "disk_usage": psutil.disk_usage("/").percent,
            "network": delta,
        }

    def _write_shared_memory(self, data: Dict):
        """写入共享内存（原子操作）"""
        print("写入共享内存")
        stats = SystemStats()
        stats.timestamp = data["timestamp"]
        stats.cpu_percent = data["cpu_percent"]
        stats.mem_total = data["memory"].total
        stats.mem_used = data["memory"].used
        stats.net_sent = data["network"]["net_sent"]
        stats.net_recv = data["network"]["net_recv"]
        stats.disk_usage = data["disk_usage"]

        with self.sem:
            self.buffer.seek(0)
            len = self.buffer.write(
                ctypes.string_at(ctypes.byref(stats), ctypes.sizeof(stats))
            )


        # def _publish_redis(self, data: Dict):
        # """发布到Redis频道"""
        # self.redis.publish(
        # CONFIG["Redis通道"],
        # json.dumps(
        #    {
        #        "timestamp": data["timestamp"],
        #        "cpu": data["cpu_percent"],
        #        "mem_used": data["memory"].used,
        #        "disk": data["disk_usage"],
        #        "net_up": data["network"]["net_sent"],
        #        "net_down": data["network"]["net_recv"],
        #    }
        # ),
        # )

    async def websocket_server(self):
        """WebSocket服务器协程"""
        async with websockets.serve(self._handle_ws, "0.0.0.0", CONFIG["WebSocket端口"]):     #添加外部访问
            await asyncio.Future()  # 永久运行

    async def _handle_ws(self, websocket):
        # """处理WebSocket连接"""
        print(f"📡 客户端已连接：{websocket.remote_address}")
        while self._running:
            data = self._collect_data()
            await websocket.send(
               json.dumps(
                   {
                       "time": datetime.now().isoformat(),
                       "cpu": data["cpu_percent"],
                       "mem": data["memory"].percent,
                       "disk": data["disk_usage"],
                       "net_up": data["network"]["net_sent"],
                       "net_down": data["network"]["net_recv"],
                   }
               )
            )
            await asyncio.sleep(CONFIG["采集间隔"])

    def run(self):
        """主运行循环"""
        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        # 启动 WebSocket 服务和数据采集作为两个协程并发运行
        async def main_loop():
            # 启动 WebSocket 服务
            ws_server_task = asyncio.create_task(self.websocket_server())

            try:
                while self._running:
                    start_time = time.time()

                    # 采集数据
                    data = self._collect_data()

                    # 写入共享内存
                    self._write_shared_memory(data)

                    # 等待采集间隔
                    elapsed = time.time() - start_time
                    await asyncio.sleep(max(0, CONFIG["采集间隔"] - elapsed))

            finally:
                self.cleanup()
                ws_server_task.cancel()
                try:
                    await ws_server_task
                except asyncio.CancelledError:
                    pass

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main_loop())
        loop.close()

        # 启动WebSocket服务
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # ws_task = loop.create_task(self.websocket_server())

        # try:
        #     while self._running:
        #         start_time = time.time()
        #
        #         # 采集数据
        #         data = self._collect_data()
        #
        #         # 写入共享内存
        #         self._write_shared_memory(data)
        #
        #         # 发布到Redis
        #         # self._publish_redis(data)
        #
        #         # 精确睡眠
        #         elapsed = time.time() - start_time
        #         sleep_time = max(0, CONFIG["采集间隔"] - elapsed)
        #         time.sleep(sleep_time)
        #
        # finally:
        #     self.cleanup()
        #     loop.run_until_complete(ws_task)
        #     loop.close()


    def signal_handler(self, signum, frame):
        """处理退出信号"""
        self._running = False
        print("\n正在清理资源...")

    def cleanup(self):
        """资源清理"""
        self.buffer.close()
        self.shm.close_fd()
        self.shm.unlink()
        self.sem.close()
        self.sem.unlink()
        # self.redis.close()


# ------------------- 主程序 -------------------
if __name__ == "__main__":
    monitor = SystemMonitor()
    print(f"🔍 系统监控已启动，数据更新间隔 {CONFIG['采集间隔']}秒")
    print(f"• 共享内存路径: {CONFIG['共享内存路径']}")
    print(f"• WebSocket端口: {CONFIG['WebSocket端口']}")
    # print(f"• Redis频道: {CONFIG['Redis通道']}")
    print("Ctrl+C 停止监控")
    monitor.run()
