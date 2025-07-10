<template>
  <div class="home-layout">
    <el-row :gutter="20">
      <!-- 左侧仪表盘：PC端占10，移动端占24 -->
      <el-col :xs="24" :sm="24" :md="10" :lg="10">
        <el-card class="card-box" shadow="hover">
          <SystemDashboard />
        </el-card>
      </el-col>

      <!-- 右侧折线图：PC端占14，移动端占24 -->
      <el-col :xs="24" :sm="24" :md="14" :lg="14">
        <el-card class="card-box" shadow="hover">
          <NetworkChart />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import SystemDashboard from '@/components/SystemDashboard.vue';
import NetworkChart from '@/components/NetworkChart.vue';

export default {
  name: 'Home',
  components: {
    SystemDashboard,
    NetworkChart
  }
};
</script>

<style scoped>
.home-layout {
  margin: 30px;
}

.card-box {
  padding: 20px;
}

/* 🔧 可选：在小屏设备下增加卡片之间的垂直间距 */
@media screen and (max-width: 768px) {
  .card-box {
    margin-bottom: 20px;
  }
}
</style>
