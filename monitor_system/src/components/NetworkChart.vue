<template>
  <div class="network-chart">
    <v-chart class="chart" :option="chartOption" autoresize />
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue';
import { use } from 'echarts/core';
import { LineChart } from 'echarts/charts';
import { GridComponent, LegendComponent, TitleComponent, TooltipComponent } from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';
import VChart from 'vue-echarts';

use([CanvasRenderer, LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);

export default defineComponent({
  name: 'NetworkChart',
  components: { VChart },

  setup() {
    const chartOption = ref({});
    const timestamps = ref([]);
    const netUpData = ref([]);
    const netDownData = ref([]);
    const MAX_POINTS = 30;

    const updateChart = () => {
      chartOption.value = {
        title: {
          text: '网络上下行速率（字节/秒）',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          top: 25,
          data: ['上行', '下行']
        },
        xAxis: {
          type: 'category',
          data: timestamps.value,
          axisLabel: { formatter: value => value.slice(11, 19) }
        },
        yAxis: {
          type: 'value',
          name: '字节/秒'
        },
        series: [
          {
            name: '上行',
            type: 'line',
            data: netUpData.value,
            smooth: true
          },
          {
            name: '下行',
            type: 'line',
            data: netDownData.value,
            smooth: true
          }
        ]
      };
    };

    const connectWebSocket = () => {
      const ws = new WebSocket('ws://192.168.3.31:8765');

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        const timeLabel = data.time.slice(11, 19); // 取时:分:秒
        timestamps.value.push(timeLabel);
        netUpData.value.push(data.net_up);
        netDownData.value.push(data.net_down);

        // 保持点数不超过 MAX_POINTS
        if (timestamps.value.length > MAX_POINTS) {
          timestamps.value.shift();
          netUpData.value.shift();
          netDownData.value.shift();
        }

        updateChart();
      };

      ws.onerror = (err) => {
        console.error('WebSocket 错误:', err);
      };

      ws.onclose = () => {
        console.warn('WebSocket 已断开');
      };
    };

    onMounted(() => {
      connectWebSocket();
    });

    return { chartOption };
  }
});
</script>

<style scoped>
.chart {
  width: 100%;
  height: 700px;
}
</style>
