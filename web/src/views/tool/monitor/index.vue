<template>
  <el-scrollbar v-loading="state.showLoading" element-loading-text="Loading..." element-loading-background="rgba(122, 122, 122, 0.9)">
    <el-scrollbar v-loading="state.showLoading" element-loading-text="Loading..." element-loading-background="rgba(122, 122, 122, 0.9)">
      <el-card class="box-card">
        <span :class="state.iconClass">系统：</span>
        <span>{{state.monitorData.system}}</span>
        <span style="margin-left: 20px">已不间断运行: {{state.monitorData.time}}</span>
        <span style="margin-left: 20px">自动刷新(秒)：</span>
        <el-input-number v-model="state.refreshInterval" size="small" :min="3" @change="restartIntervalMonitor"/>
        <el-button style="margin-left: 20px" type="primary" v-show="state.timer" :text="true" link @click="handleServer"><span style="font-size: 13px"  @click="clearIntervalMonitor">停止</span></el-button>
        <el-button style="margin-left: 20px" type="primary" v-show="!state.timer" :text="true" link @click="handleServer"><span style="font-size: 13px"  @click="restartIntervalMonitor">开始</span></el-button>
        <el-button type="primary" :text="true" link @click="handleServer"><span style="font-size: 13px">手动刷新</span></el-button>
      </el-card>
      <el-card class="box-card">
        <StatusCard  v-model="state.monitorData"></StatusCard>
      </el-card>
      <el-card class="box-card">
<!--        <EchartCard  v-model="state.monitorData.network"></EchartCard>-->
      </el-card>
    </el-scrollbar>
  </el-scrollbar>
</template>

<script setup lang="ts">
import {reactive, onMounted, onUnmounted} from "vue";
import { getServer } from "@/api/tool/monitor";
import {ElMessage} from "element-plus";
import StatusCard from "./component/statusCard.vue";

const state = reactive({
  showLoading:false,
  iconClass:'',
  monitorData:{
    cpu: [0, 0, [0, 0, 0, 0], "", 0, 1],
    disk: [{path: "", size: ["0GB", "0GB", "0GB", 0], inodes: false}],
    is_windows: true,
    load_average: {one: 0, five: 0, fifteen: 0, max: 0, limit: 0, safe:0, percent: 0},
    mem: {percent: 0, total: 0, free: 0, used: 0},
    system: "",
    time: "0天",
    network:{
      up:0,
      down:0,
      downTotal:0,
      upTotal:0,
      network:{
      }
    }
  },
  refreshInterval:3,
  timer:null,//定时器
});
// 获取数据
const handleServer = () => {
  getServer().then((res: any) => {
    if (res.code == 200) {
      state.monitorData = res.data;
      let tempsystem = res.data.system.split(" ")[0].toLowerCase()
      state.iconClass = 'ico-'+tempsystem
    } else {
      ElMessage.error("获取服务信息失败");
    }
  });
};
const intervalMonitor = () => {
  state.timer = setInterval(() => {
    handleServer();
  }, state.refreshInterval * 1000);
};

const restartIntervalMonitor = () => {
  clearIntervalMonitor();
  intervalMonitor();
};

const clearIntervalMonitor = () => {
  clearInterval(state.timer);
  state.timer = null;
};
onMounted(() => {
  handleServer();
});

onUnmounted(() => {
  clearIntervalMonitor();
});
</script>

<style scoped>
</style>
