<template>
  <div class="h100" v-show="!isTagsViewCurrenFull">
    <el-aside class="layout-aside" :class="setCollapseStyle">
      <Logo v-if="setShowLogo" />
      <el-scrollbar
        class="flex-auto"
        ref="layoutAsideScrollbarRef"
        @mouseenter="onAsideEnterLeave(true)"
        @mouseleave="onAsideEnterLeave(false)"
      >
        <Vertical :menuList="menuList" />
      </el-scrollbar>
    </el-aside>
  </div>
</template>

<script setup lang="ts" name="layoutAside">
import {
  ref,
  reactive,
  toRefs,
  computed,
  watch,
  getCurrentInstance,
  onBeforeMount,
} from "vue";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useRoutesListStore } from "@/stores/routesList";
import { useTagsViewRoutesStore } from "@/stores/tagsViewRoutes";
import Logo from "@/layout/logo/index.vue";
import Vertical from "@/layout/navMenu/vertical.vue";

const { proxy } = getCurrentInstance() as any;
const theme = useThemeConfigStateStore();
const routesList = useRoutesListStore();
const tagsViewRoutes = useTagsViewRoutesStore();
const layoutAsideScrollbarRef = ref<any>(null);

const state: any = reactive({
  menuList: [],
  clientWidth: "",
});

const { menuList } = toRefs(state);

// 获取布局配置信息
const getThemeConfig = computed(() => theme.themeConfig);

// 获取卡片全屏信息
const isTagsViewCurrenFull = computed(() => tagsViewRoutes.isTagsViewCurrenFull);

// 设置菜单展开/收起时的宽度
const setCollapseStyle = computed(() => {
  const { layout, isCollapse, menuBar } = theme.themeConfig;
  const asideBrColor =
    menuBar === "#FFFFFF" ||
    menuBar === "#FFF" ||
    menuBar === "#fff" ||
    menuBar === "#ffffff"
      ? "layout-el-aside-br-color"
      : "";
  if (layout === "columns") {
    if (isCollapse) {
      return [asideBrColor, "layout-aside-pc-1"];
    } else {
      return [asideBrColor, "layout-aside-pc-220"];
    }
  } else {
    if (isCollapse) {
      return [asideBrColor, "layout-aside-pc-64"];
    } else {
      return [asideBrColor, "layout-aside-pc-220"];
    }
  }
});

// 设置显示/隐藏 logo
const setShowLogo = computed(() => {
  let { layout, isShowLogo } = theme.themeConfig;
  return (isShowLogo && layout === "defaults") || (isShowLogo && layout === "columns");
});

// 关闭移动端蒙版
const closeLayoutAsideMobileMode = () => {
  const el = document.querySelector(".layout-aside-mobile-mode");
  el && el.parentNode?.removeChild(el);
  const clientWidth = document.body.clientWidth;
  if (clientWidth < 1000) theme.themeConfig.isCollapse = false;
  document.body.setAttribute("class", "");
};

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

// 设置/过滤路由（非静态路由/是否显示在菜单中）
const setFilterRoutes = () => {
  if (theme.themeConfig.layout === "columns") return false;
  state.menuList = filterRoutesFun(routesList.routesList);
};

// 设置菜单导航是否固定（移动端）
const initMenuFixed = (clientWidth: number) => {
  state.clientWidth = clientWidth;
};

// 鼠标移入、移出
const onAsideEnterLeave = (bool: Boolean) => {
  let { layout } = theme.themeConfig;
  if (layout !== "columns") return false;
  if (!bool) proxy.mittBus.emit("restoreDefault");
  routesList.setColumnsMenuHover(bool);
};

// 监听 themeConfig 配置文件的变化，更新菜单 el-scrollbar 的高度
watch(theme.themeConfig, (val) => {
  if (val.isShowLogoChange !== val.isShowLogo) {
    layoutAsideScrollbarRef.value?.update?.();
  }
});

// 监听vuex值的变化，动态赋值给菜单中
theme.$subscribe((mutations, val) => {
  let { layout, isClassicSplitMenu } = val.themeConfig;
  if (layout === "classic" && isClassicSplitMenu) return false;
  setFilterRoutes();
});

// 页面加载前
onBeforeMount(() => {
  initMenuFixed(document.body.clientWidth);
  setFilterRoutes();
  proxy.mittBus.on("setSendColumnsChildren", (res: any) => {
    state.menuList = res.children;
  });
  proxy.mittBus.on("setSendClassicChildren", (res: any) => {
    let { layout, isClassicSplitMenu } = theme.themeConfig;
    if (layout === "classic" && isClassicSplitMenu) {
      state.menuList = [];
      state.menuList = res.children;
    }
  });
  proxy.mittBus.on("getBreadcrumbIndexSetFilterRoutes", () => {
    setFilterRoutes();
  });
  proxy.mittBus.on("layoutMobileResize", (res: any) => {
    initMenuFixed(res.clientWidth);
    closeLayoutAsideMobileMode();
  });
});
</script>
