<template>
  <div class="home-container">
    <el-row :gutter="15">
      <el-col :sm="6" class="mb15">
        <div class="home-card-item home-card-first">
          <div class="flex-margin flex">
            <img :src="getUserInfos.photo" />
            <div class="home-card-first-right ml15">
              <div class="flex-margin">
                <div class="home-card-first-right-title">
                  {{ currentTime }}，{{
                    getUserInfos.username === "" ? "test" : getUserInfos.username
                  }}！
                </div>
                <div class="home-card-first-right-msg mt5">
                  {{ getUserInfos.username === "admin" ? "超级管理" : "普通用户" }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :sm="6" class="mb15" v-for="(v, k) in state.topCardItemList" :key="k">
        <div class="home-card-item home-card-item-box" :style="{ background: v.color }">
          <div class="home-card-item-flex">
            <div class="home-card-item-title pb3">{{ v.title }}</div>
            <div class="home-card-item-title-num pb6">{{ v.titleNum }}</div>
            <div class="home-card-item-tip pb3">{{ v.tip }}</div>
            <div class="home-card-item-tip-num">{{ v.tipNum }}</div>
          </div>
          <i :class="v.icon" :style="{ color: v.iconColor }"></i>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="15">
      <el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16" class="mb15">
        <el-card shadow="hover" :header="$t('message.card.title1')">
          <div style="height: 200px" ref="homeLaboratoryRef"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8">
        <el-card shadow="hover" :header="$t('message.card.title2')">
          <div class="home-monitor">
            <div class="flex-warp">
              <div
                class="flex-warp-item"
                v-for="(v, k) in state.environmentList"
                :key="k"
              >
                <div class="flex-warp-item-box">
                  <i :class="v.icon" :style="{ color: v.iconColor }"></i>
                  <span class="pl5">{{ v.label }}</span>
                  <div class="mt10">
                    <a v-if="v.link" :href="v.link" target="_blank">{{ v.value }}</a>
                    <span v-else>{{ v.value }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="15">
      <el-col :xs="24" :sm="14" :md="14" :lg="16" :xl="16" class="home-warning-media">
        <el-card
          shadow="hover"
          :header="$t('message.card.title3')"
          class="home-warning-card"
        >
          <el-table :data="state.tableData.data" style="width: 100%" stripe>
            <el-table-column
              prop="date"
              :label="$t('message.table.th1')"
            ></el-table-column>
            <el-table-column
              prop="name"
              :label="$t('message.table.th2')"
            ></el-table-column>
            <el-table-column
              prop="address"
              :label="$t('message.table.th3')"
            ></el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="10" :md="10" :lg="8" :xl="8" class="home-dynamic-media">
        <el-card shadow="hover" :header="$t('message.card.title4')">
          <div class="home-dynamic">
            <el-scrollbar>
              <div
                class="home-dynamic-item"
                v-for="(v, k) in state.activitiesList"
                :key="k"
              >
                <div class="home-dynamic-item-left">
                  <div class="home-dynamic-item-left-time1 mb5">{{ v.time1 }}</div>
                  <div class="home-dynamic-item-left-time2">{{ v.time2 }}</div>
                </div>
                <div class="home-dynamic-item-line">
                  <i class="iconfont icon-fangkuang"></i>
                </div>
                <div class="home-dynamic-item-right">
                  <div class="home-dynamic-item-right-title mb5">
                    <SvgIcon name="elementComment" />
                    <span>{{ v.title }}</span>
                  </div>
                  <div class="home-dynamic-item-right-label">{{ v.label }}</div>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24" class="mt15">
        <el-card shadow="hover" :header="$t('message.card.title5')">
          <div style="height: 200px" ref="homeOvertimeRef"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import {
  reactive,
  onMounted,
  nextTick,
  computed,
  getCurrentInstance,
  watch,
  onActivated,
} from "vue";
import * as echarts from "echarts";
import { CountUp } from "countup.js";
import { formatAxis } from "@/utils/formatTime";
import { useTagsViewRoutesStore } from "@/stores/tagsViewRoutes";
import { useUserInfosState } from "@/stores/userInfos";
import { topCardItemList, environmentList, activitiesList } from "./mock";

const { proxy } = getCurrentInstance() as any;

const tagsViewRoutes = useTagsViewRoutesStore();
const userInfos = useUserInfosState();
const state = reactive({
  topCardItemList,
  environmentList,
  activitiesList,
  tableData: {
    data: [
      {
        date: "2025-01-01",
        name: "爬虫管理平台",
        address: "TaskPyro",
      },
      {
        date: "2025-02-01",
        name: "Django-admin-vue3管理平台",
        address: "Django-admin-vue3管理平台",
      },
      {
        date: "2025-03-01",
        name: "和鲸社区创作者",
        address: "https://www.heywhale.com/home/user/profile/5eef5c2435465c002d90c878",
      },
    ],
  },
  myCharts: [],
});
// 获取用户信息 pinia
const getUserInfos = computed(() => {
  return userInfos.userInfos;
});
// 当前时间提示语
const currentTime = computed(() => {
  return formatAxis(new Date());
});

// 项目统计
const initHomeLaboratory = () => {
  const myChart = echarts.init(proxy.$refs.homeLaboratoryRef);
  const option = {
    grid: {
      top: 50,
      right: 20,
      bottom: 30,
      left: 30,
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["项目活跃度", "代码提交量"],
      right: 13,
    },
    xAxis: {
      data: [
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
      ],
    },
    yAxis: [
      {
        type: "value",
        name: "数量",
      },
    ],
    series: [
      {
        name: "项目活跃度",
        type: "bar",
        data: [20, 25, 32, 45, 50, 65, 71, 85, 95, 105, 115, 121],
        itemStyle: {
          barBorderRadius: [4, 4, 0, 0],
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: "linear",
            global: false,
            colorStops: [
              {
                offset: 0,
                color: "#3DD2B4",
              },
              {
                offset: 1,
                color: "#63caff",
              },
            ],
          },
        },
      },
      {
        name: "代码提交量",
        type: "line",
        data: [15, 18, 22, 35, 42, 55, 62, 75, 82, 90, 95, 100],
        itemStyle: {
          color: "#E88662",
        },
      },
    ],
  };
  myChart.setOption(option);
  state.myCharts.push(myChart);
};
// 项目活动统计
const initHomeOvertime = () => {
  const myChart = echarts.init(proxy.$refs.homeOvertimeRef);
  const option = {
    grid: {
      top: 50,
      right: 20,
      bottom: 30,
      left: 30,
    },
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: ["开源项目", "技术文章", "平台用户", "活跃贡献"],
      right: 13,
    },
    xAxis: {
      data: [
        "1月",
        "2月",
        "3月",
        "4月",
        "5月",
        "6月",
        "7月",
        "8月",
        "9月",
        "10月",
        "11月",
        "12月",
      ],
    },
    yAxis: [
      {
        type: "value",
        name: "数量",
      },
    ],
    series: [
      {
        name: "开源项目",
        type: "bar",
        data: [2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9, 10],
      },
      {
        name: "技术文章",
        type: "bar",
        data: [5, 8, 12, 15, 20, 25, 30, 35, 40, 43, 47, 50],
      },
      {
        name: "平台用户",
        type: "line",
        data: [10, 15, 25, 35, 45, 55, 65, 75, 82, 88, 95, 100],
      },
      {
        name: "活跃贡献",
        type: "line",
        data: [5, 8, 12, 18, 25, 32, 38, 45, 52, 58, 65, 72],
      },
    ],
  };
  myChart.setOption(option);
  state.myCharts.push(myChart);
};
// 批量设置 echarts resize
const initEchartsResizeFun = () => {
  nextTick(() => {
    for (let i = 0; i < state.myCharts.length; i++) {
      state.myCharts[i].resize();
    }
  });
};
// 批量设置 echarts resize
const initEchartsResize = () => {
  window.addEventListener("resize", initEchartsResizeFun);
};
// 页面加载时
onMounted(() => {
  initHomeLaboratory();
  initHomeOvertime();
  initEchartsResize();
});
// 由于页面缓存原因，keep-alive
onActivated(() => {
  initEchartsResizeFun();
});
// 监听 vuex 中的 tagsview 开启全屏变化，重新 resize 图表，防止不出现/大小不变等
watch(
  () => tagsViewRoutes.isTagsViewCurrenFull,
  () => {
    initEchartsResizeFun();
  }
);
</script>

<style scoped lang="scss">
.home-container {
  overflow-x: hidden;
  .home-card-item {
    width: 100%;
    height: 103px;
    background: var(--el-text-color-secondary);
    border-radius: 15px;
    transition: all ease 0.3s;
    &:hover {
      box-shadow: 0 2px 12px 0 rgb(0 0 0 / 10%);
      transition: all ease 0.3s;
    }
  }
  .home-card-item-box {
    display: flex;
    align-items: center;
    position: relative;
    overflow: hidden;
    &:hover {
      i {
        right: 0px !important;
        bottom: 0px !important;
        transition: all ease 0.3s;
      }
    }
    i {
      position: absolute;
      right: -10px;
      bottom: -10px;
      font-size: 70px;
      transform: rotate(-30deg);
      transition: all ease 0.3s;
    }
    .home-card-item-flex {
      padding: 0 20px;
      color: var(--color-whites);
      .home-card-item-title,
      .home-card-item-tip {
        font-size: 13px;
      }
      .home-card-item-title-num {
        font-size: 18px;
      }
      .home-card-item-tip-num {
        font-size: 13px;
      }
    }
  }
  .home-card-first {
    background: var(--el-color-white);
    border: 1px solid var(--el-border-color-light, #ebeef5);
    display: flex;
    align-items: center;
    img {
      width: 60px;
      height: 60px;
      border-radius: 100%;
      border: 2px solid var(--color-primary-light-5);
    }
    .home-card-first-right {
      flex: 1;
      display: flex;
      flex-direction: column;
      .home-card-first-right-title {
        color: var(--el-color-black);
      }
      .home-card-first-right-msg {
        font-size: 13px;
        color: var(--el-text-color-secondary);
      }
    }
  }
  .home-monitor {
    height: 200px;
    .flex-warp-item {
      width: 50%;
      height: 100px;
      display: flex;
      .flex-warp-item-box {
        margin: auto;
        height: auto;
        text-align: center;
        color: var(--el-text-color-primary);
      }
    }
  }
  .home-warning-card {
    height: 292px;
    ::v-deep(.el-card) {
      height: 100%;
    }
  }
  .home-dynamic {
    height: 200px;
    .home-dynamic-item {
      display: flex;
      width: 100%;
      height: 60px;
      overflow: hidden;
      &:first-of-type {
        .home-dynamic-item-line {
          i {
            color: orange !important;
          }
        }
      }
      .home-dynamic-item-left {
        text-align: right;
        .home-dynamic-item-left-time1 {
        }
        .home-dynamic-item-left-time2 {
          font-size: 13px;
          color: var(--el-text-color-secondary);
        }
      }
      .home-dynamic-item-line {
        height: 60px;
        border-right: 2px dashed var(--el-border-color-light, #ebeef5);
        margin: 0 20px;
        position: relative;
        i {
          color: var(--color-primary);
          font-size: 12px;
          position: absolute;
          top: 1px;
          left: -6px;
          transform: rotate(46deg);
          background: var(--el-color-white);
        }
      }
      .home-dynamic-item-right {
        flex: 1;
        .home-dynamic-item-right-title {
          i {
            margin-right: 5px;
            border: 1px solid var(--el-border-color-light, #ebeef5);
            width: 20px;
            height: 20px;
            border-radius: 100%;
            padding: 3px 2px 2px;
            text-align: center;
            color: var(--color-primary);
          }
        }
        .home-dynamic-item-right-label {
          font-size: 13px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}
</style>
