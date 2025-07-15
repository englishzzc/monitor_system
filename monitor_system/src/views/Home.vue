<template>
  <div class="home-layout">
    <el-row :gutter="20">
      <!-- 左侧仪表盘卡片（占比4） -->
      <el-col :xs="24" :sm="24" :md="10" :lg="10">
        <el-card class="card-box" shadow="hover">
          <template #header>
            <span>
              <i class="el-icon-s-data" style="margin-right: 6px;" />
              系统仪表盘
            </span>
          </template>
          <SystemDashboard />
        </el-card>
      </el-col>

      <!-- 右侧网络速率卡片（占比6） -->
      <el-col :xs="24" :sm="24" :md="14" :lg="14">
        <el-card class="card-box" shadow="hover">
          <template #header>
            <span>
              <i class="el-icon-share" style="margin-right: 6px;" />
              网络上下行速率
            </span>
          </template>
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
  min-height: 100%;
}

/* 移动端卡片间距 */
@media screen and (max-width: 768px) {
  .card-box {
    margin-bottom: 20px;
  }
}
</style>
