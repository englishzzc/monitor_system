import Vue from 'vue'
import ElementUI from 'element-ui';//添加
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios';
import VueAxios from 'vue-axios';
import "echarts";
import ECharts from 'vue-echarts';


Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.component('ECharts',ECharts)

Vue.use(VueAxios , axios)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
