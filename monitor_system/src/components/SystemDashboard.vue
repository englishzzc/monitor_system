<!-- <template>
  <div class="dashboard">
    <div class="chart-wrapper">
      <v-chart class="chart" :option="cpuOption" autoresize />
      <div class="info-text">CPU 使用率：{{ cpu.toFixed(1) }}%</div>
    </div>

    <div class="chart-wrapper">
      <v-chart class="chart" :option="memOption" autoresize />
      <div class="info-text">内存使用率：{{ mem.toFixed(1) }}%</div>
    </div>

    <div class="chart-wrapper">
      <v-chart class="chart" :option="diskOption" autoresize />
      <div class="info-text">磁盘使用率：{{ disk.toFixed(1) }}%</div>
    </div>
  </div>
</template>


<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { use } from 'echarts/core';
import { GaugeChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

use([CanvasRenderer, GaugeChart, TitleComponent, TooltipComponent]);

export default {
  name: 'SystemDashboard',
  components: { VChart },
  setup() {
    const cpu = ref(0);
    const mem = ref(0);
    const disk = ref(0);

    const cpuOption = ref({});
    const memOption = ref({});
    const diskOption = ref({});

    let ws = null;

    const updateCharts = () => {
      cpuOption.value = {
        title: { text: 'CPU 使用率', left: 'center', top: '5%' },
        series: [{
          type: 'gauge',
          progress: { show: true },
          detail: { valueAnimation: true, formatter: '{value}%' },
          data: [{ value: cpu.value }],
        }],
      };
      memOption.value = {
        title: { text: '内存使用率', left: 'center', top: '5%' },
        series: [{
          type: 'gauge',
          progress: { show: true },
          detail: { valueAnimation: true, formatter: '{value}%' },
          data: [{ value: mem.value }],
        }],
      };
      diskOption.value = {
        title: { text: '磁盘使用率', left: 'center', top: '5%' },
        series: [{
          type: 'gauge',
          progress: { show: true },
          detail: { valueAnimation: true, formatter: '{value}%' },
          data: [{ value: disk.value }],
        }],
      };
    };

    onMounted(() => {
      ws = new WebSocket("ws://192.168.3.31:8765");

      ws.onopen = () => {
        console.log("✅ WebSocket 已连接");
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        cpu.value = data.cpu;
        mem.value = data.mem;
        disk.value = data.disk;
        updateCharts();
      };

      ws.onerror = (err) => {
        console.error("❌ WebSocket 错误", err);
      };

      ws.onclose = () => {
        console.log("❌ WebSocket 已关闭");
      };
    });

    onBeforeUnmount(() => {
      if (ws) ws.close();
    });

    return {
      cpu,
      mem,
      disk,
      cpuOption,
      memOption,
      diskOption,
    };
  }
};
</script>


<style scoped>
.dashboard {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.chart-wrapper {
  width: 30%;
  margin: 1em;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 100%;
  height: 300px;
}

.info-text {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
  text-align: center;
}
</style> -->


<template>
  <div class="dashboard">
    <!-- CPU 仪表盘 -->
    <div class="chart-wrapper">
      <v-chart class="chart" :option="cpuOption" autoresize />
      <div class="info-text">CPU 使用率：{{ cpu.toFixed(1) }}%</div>
    </div>

    <!-- 内存仪表盘 -->
    <div class="chart-wrapper">
      <v-chart class="chart" :option="memOption" autoresize />
      <div class="info-text">内存使用率：{{ mem.toFixed(1) }}%</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { use } from 'echarts/core';
import { GaugeChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

use([CanvasRenderer, GaugeChart, TitleComponent, TooltipComponent]);

export default {
  name: 'SystemDashboard',
  components: { VChart },

  setup() {
    const cpu = ref(0);
    const mem = ref(0);

    const cpuOption = ref({});
    const memOption = ref({});
    let ws = null;

    const updateCharts = () => {
      cpuOption.value = {
        title: { text: 'CPU 使用率', left: 'center', top: '5%' },
        series: [{
          type: 'gauge',
          progress: { show: true },
          detail: { valueAnimation: true, formatter: '{value}%' },
          data: [{ value: cpu.value }],
        }],
      };

      memOption.value = {
        title: { text: '内存使用率', left: 'center', top: '5%' },
        series: [{
          type: 'gauge',
          progress: { show: true },
          detail: { valueAnimation: true, formatter: '{value}%' },
          data: [{ value: mem.value }],
        }],
      };
    };

    onMounted(() => {
      ws = new WebSocket('ws://192.168.3.31:8765');

      ws.onopen = () => console.log('✅ WebSocket 已连接');
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        cpu.value = data.cpu;
        mem.value = data.mem;
        updateCharts();
      };
      ws.onerror = (err) => console.error('❌ WebSocket 错误', err);
      ws.onclose = () => console.log('❌ WebSocket 已关闭');
    });

    onBeforeUnmount(() => {
      if (ws) ws.close();
    });

    return {
      cpu,
      mem,
      cpuOption,
      memOption
    };
  }
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column; /* ✅ 改为垂直排列 */
  align-items: center;
  justify-content: start;
  gap: 20px;
}

.chart-wrapper {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart {
  width: 100%;
  height: 300px;
}

.info-text {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
  text-align: center;
}
</style>
