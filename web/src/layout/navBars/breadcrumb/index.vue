<template>
  <div class="layout-navbars-breadcrumb-index">
    <Logo v-if="setIsShowLogo" />
    <Breadcrumb />
    <Horizontal :menuList="menuList" v-if="isLayoutTransverse" />
    <User />
  </div>
</template>

<script setup lang="ts" name="layoutBreadcrumbIndex">
import {
  computed,
  ref,
  onMounted,
  onUnmounted,
  getCurrentInstance,
} from "vue";
import { useRoute } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useRoutesListStore } from "@/stores/routesList";
import Breadcrumb from "@/layout/navBars/breadcrumb/breadcrumb.vue";
import User from "@/layout/navBars/breadcrumb/user.vue";
import Logo from "@/layout/logo/index.vue";
import Horizontal from "@/layout/navMenu/horizontal.vue";

const { proxy } = getCurrentInstance() as any;
const theme = useThemeConfigStateStore();
const routesList = useRoutesListStore();
const route = useRoute();
const menuList = ref<any[]>([]);

// 设置 logo 显示/隐藏
const setIsShowLogo = computed(() => {
  let { isShowLogo, layout } = theme.themeConfig;
  return (
    (isShowLogo && layout === "classic") || (isShowLogo && layout === "transverse")
  );
});

// 设置是否显示横向导航菜单
const isLayoutTransverse = computed(() => {
  let { layout, isClassicSplitMenu } = theme.themeConfig;
  return layout === "transverse" || (isClassicSplitMenu && layout === "classic");
});

// 路由过滤递归函数
const filterRoutesFun = (arr: Array<object>): any[] => {
  return arr
    .filter((item: any) => !item.meta?.isHide)
    .map((item: any) => {
      item = Object.assign({}, item);
      if (item.children) item.children = filterRoutesFun(item.children);
      return item;
    });
};

// 设置了分割菜单时，删除底下 children
const delClassicChildren = (arr: Array<object>) => {
  arr.forEach((v: any) => {
    if (v.children) delete v.children;
  });
  return arr;
};

// 传送当前子级数据到菜单中
const setSendClassicChildren = (path: string) => {
  const currentPathSplit = path.split("/");
  let currentData: any = {};
  filterRoutesFun(routesList.routesList).forEach((v, k) => {
    if (v.path === `/${currentPathSplit[1]}`) {
      v["k"] = k;
      currentData["item"] = [{ ...v }];
      currentData["children"] = v.children ? v.children : [{ ...v }];
    }
  });
  return currentData;
};

// 设置/过滤路由（非静态路由/是否显示在菜单中）
const setFilterRoutes = () => {
  let { layout, isClassicSplitMenu } = theme.themeConfig;
  if (layout === "classic" && isClassicSplitMenu) {
    menuList.value = delClassicChildren(
      filterRoutesFun(routesList.routesList)
    );
    const resData = setSendClassicChildren(route.path);
    proxy.mittBus.emit("setSendClassicChildren", resData);
  } else {
    menuList.value = filterRoutesFun(routesList.routesList);
  }
};

onMounted(() => {
  setFilterRoutes();
  proxy.mittBus.on("getBreadcrumbIndexSetFilterRoutes", () => {
    setFilterRoutes();
  });
});

onUnmounted(() => {
  proxy.mittBus.off("getBreadcrumbIndexSetFilterRoutes");
});
</script>

<style scoped lang="scss">
.layout-navbars-breadcrumb-index {
  height: 51px;
  display: flex;
  align-items: center;
  padding-right: 15px;
  background: var(--bg-topBar);
  border-bottom: 1px solid #f1f2f3;
}
</style>
