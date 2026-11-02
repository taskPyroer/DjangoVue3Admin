<template>
  <div class="layout-navbars-breadcrumb" :style="{ display: isShowBreadcrumb }">
    <SvgIcon
      class="layout-navbars-breadcrumb-icon"
      :name="getThemeConfig.isCollapse ? 'elementExpand' : 'elementFold'"
      @click="onThemeConfigChange"
    />
    <el-breadcrumb class="layout-navbars-breadcrumb-hide">
      <transition-group name="breadcrumb" v-bind="$attrs">
        <el-breadcrumb-item v-for="(v, k) in breadcrumbList" :key="v.meta.title">
          <span
            v-if="k === breadcrumbList.length - 1"
            class="layout-navbars-breadcrumb-span"
          >
            <SvgIcon
              :name="v.meta.icon"
              :size="16"
              class="layout-navbars-breadcrumb-iconfont"
              v-if="getThemeConfig.isBreadcrumbIcon"
            />{{ $t(v.meta.title) }}
          </span>
          <a v-else @click.prevent="onBreadcrumbClick(v)">
            <SvgIcon
              :name="v.meta.icon"
              :size="16"
              class="layout-navbars-breadcrumb-iconfont"
              v-if="getThemeConfig.isBreadcrumbIcon"
            />{{ $t(v.meta.title) }}
          </a>
        </el-breadcrumb-item>
      </transition-group>
    </el-breadcrumb>
  </div>
</template>

<script setup lang="ts" name="layoutBreadcrumb">
import { toRefs, reactive, computed, getCurrentInstance, onMounted } from "vue";
import { onBeforeRouteUpdate, useRoute, useRouter } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useRoutesListStore } from "@/stores/routesList";
import { storeToRefs } from 'pinia';

const { proxy } = getCurrentInstance() as any;
const route = useRoute();
const router = useRouter();
const theme = useThemeConfigStateStore();
const stores = useRoutesListStore();
const { routesList } = storeToRefs(stores);

const state: any = reactive({
  breadcrumbList: [],
  routeSplit: [],
  routeSplitFirst: "",
  routeSplitIndex: 1,
});

const { breadcrumbList } = toRefs(state);

// 获取布局配置信息
const getThemeConfig = computed(() => theme.themeConfig);

// 展开/收起左侧菜单点击
const onThemeConfigChange = () => {
  proxy.mittBus.emit("onMenuClick");
  theme.themeConfig.isCollapse = !theme.themeConfig.isCollapse;
};

// 面包屑点击时
const onBreadcrumbClick = (v: any) => {
  const { redirect, path } = v;
  if (redirect) router.push(redirect);
  else router.push(path);
};

// 处理面包屑数据
const getBreadcrumbList = (arr: Array<object>) => {
  arr.forEach((item: any) => {
    state.routeSplit.forEach((v: any, k: number, arrs: any) => {
      if (state.routeSplitFirst === item.path) {
        state.routeSplitFirst += `/${arrs[state.routeSplitIndex]}`;
        state.breadcrumbList.push(item);
        state.routeSplitIndex++;
        if (item.children) getBreadcrumbList(item.children);
      }
    });
  });
};

// 当前路由字符串切割成数组，并删除第一项空内容
const initRouteSplit = (path: string) => {
  if (!theme.themeConfig.isBreadcrumb) return false;

  state.breadcrumbList = [routesList.value[0]];
  state.routeSplit = path.split("/");
  state.routeSplit.shift();
  state.routeSplitFirst = `/${state.routeSplit[0]}`;
  state.routeSplitIndex = 1;
  getBreadcrumbList(routesList.value);
};

// 动态设置经典、横向布局不显示
const isShowBreadcrumb = computed(() => {
  initRouteSplit(route.path);
  const { layout, isBreadcrumb } = theme.themeConfig;
  if (layout === "classic" || layout === "transverse") {
    return "none";
  } else {
    return isBreadcrumb ? "" : "none";
  }
});

onMounted(() => {
  initRouteSplit(route.path);
});

onBeforeRouteUpdate((to) => {
  initRouteSplit(to.path);
});
</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb {
  flex: 1;
  height: inherit;
  display: flex;
  align-items: center;
  padding-left: 15px;
  .layout-navbars-breadcrumb-icon {
    cursor: pointer;
    font-size: 18px;
    margin-right: 15px;
    color: var(--bg-topBarColor);
  }
  .layout-navbars-breadcrumb-span {
    opacity: 0.7;
    color: var(--bg-topBarColor);
  }
  .layout-navbars-breadcrumb-iconfont {
    font-size: 14px;
    margin-right: 5px;
  }
  :deep(.el-breadcrumb__separator) {
    opacity: 0.7;
    color: var(--bg-topBarColor);
  }
}
</style>
