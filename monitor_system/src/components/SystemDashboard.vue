<template>
  <div class="dashboard">
    <!-- CPU 仪表盘 + 说明 -->
    <div class="chart-wrapper">
      <v-chart class="chart" :option="cpuOption" autoresize />
      <div class="info-text">
        当前 CPU 使用率：{{ cpuPercent.toFixed(1) }}%
      </div>
    </div>

    <!-- 内存仪表盘 + 总量说明 -->
    <div class="chart-wrapper">
      <v-chart class="chart" :option="memoryOption" autoresize />
      <div class="info-text">
        使用内存：{{ memUsedMB.toFixed(1) }} MB / 总内存：{{ memTotalMB.toFixed(1) }} MB
      </div>
    </div>
  </div>
</template>


<script>
import { ref, defineComponent, onMounted } from 'vue';
import { use } from 'echarts/core';
import { GaugeChart } from 'echarts/charts';
import { TooltipComponent, TitleComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

use([CanvasRenderer, GaugeChart, TooltipComponent, TitleComponent]);

export default defineComponent({
  name: 'SystemDashboard',
  components: { VChart },

  setup() {
    const cpuOption = ref({});
    const memoryOption = ref({});
    const memUsedMB = ref(0);
    const memTotalMB = ref(0);
    const cpuPercent = ref(0);

    const updateData = () => {
      const fakeData = {
        cpu_percent: 37.5,
        mem_total: 8 * 1024 * 1024 * 1024,
        mem_used: 3.2 * 1024 * 1024 * 1024,
      };

      cpuPercent.value = fakeData.cpu_percent;
      memUsedMB.value = fakeData.mem_used / 1024 / 1024;
      memTotalMB.value = fakeData.mem_total / 1024 / 1024;

      cpuOption.value = {
        title: { text: 'CPU 使用率', left: 'center', top: '2%' },
        series: [
          {
            type: 'gauge',
            progress: { show: true },
            detail: { valueAnimation: true, formatter: '{value}%' },
            data: [{ value: fakeData.cpu_percent }],
          },
        ],
      };

      memoryOption.value = {
        title: { text: '内存使用率', left: 'center', top: '2%' },
        series: [
          {
            type: 'gauge',
            progress: { show: true },
            detail: {
              valueAnimation: true,
              formatter: '{value}%', // 只显示百分比
            },
            data: [
              {
                value: ((fakeData.mem_used / fakeData.mem_total) * 100).toFixed(1),
              },
            ],
          },
        ],
      };
    };

    onMounted(() => {
      updateData();
    });

    return {
      cpuOption,
      memoryOption,
      memUsedMB,
      memTotalMB,
      cpuPercent, // 👈 补上这个
    };
  },
});

</script>

<style scoped>
.dashboard {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
.chart-wrapper {
  width: 45%;
  margin: 1em;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.chart {
  width: 100%;
  height: 350px; /* 稍微加高图表高度 */
}
.info-text {
  margin-top: 10px; /* 保证图表下方留白 */
  font-size: 14px;
  color: #666;
  text-align: center;
}

</style>
