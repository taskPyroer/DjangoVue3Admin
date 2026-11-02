<template>
  <div class="el-menu-horizontal-warp">
    <el-scrollbar
      @wheel.prevent="onElMenuHorizontalScroll"
      ref="elMenuHorizontalScrollRef"
    >
      <el-menu
        router
        :default-active="defaultActive"
        :ellipsis="false"
        background-color="transparent"
        mode="horizontal"
      >
        <template v-for="val in menuLists">
          <el-sub-menu
            :index="val.path"
            v-if="val.children && val.children.length > 0"
            :key="val.path"
          >
            <template #title>
              <SvgIcon :name="val.meta.icon" />
              {{ $t(val.meta.title) }}
            </template>
            <SubItem :chil="val.children" />
          </el-sub-menu>
          <el-menu-item :index="val.path" :key="val.path" v-else>
            <template
              #title
              v-if="!val.meta.isLink || (val.meta.isLink && val.meta.isIframe)"
            >
              <SvgIcon :name="val.meta.icon" />
              {{ $t(val.meta.title) }}
            </template>
            <template #title v-else>
              <a :href="val.meta.isLink" target="_blank" rel="opener">
                <SvgIcon :name="val.meta.icon" />
                {{ $t(val.meta.title) }}
              </a>
            </template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts" name="navMenuHorizontal">
import {
  ref,
  computed,
  getCurrentInstance,
  onMounted,
  nextTick,
  onBeforeMount,
} from "vue";
import { useRoute, onBeforeRouteUpdate } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useRoutesListStore } from "@/stores/routesList";
import SubItem from "@/layout/navMenu/subItem.vue";

const props = withDefaults(
  defineProps<{
    menuList?: any[];
  }>(),
  {
    menuList: () => [],
  }
);

const { proxy } = getCurrentInstance() as any;
const route = useRoute();
const theme = useThemeConfigStateStore();
const routesList = useRoutesListStore();

const elMenuHorizontalScrollRef = ref<any>(null);
const defaultActive = ref<any>(null);

// 获取父级菜单数据
const menuLists = computed(() => props.menuList);

// 设置横向滚动条可以鼠标滚轮滚动
const onElMenuHorizontalScroll = (e: any) => {
  const eventDelta = e.wheelDelta || -e.deltaY * 40;
  if (elMenuHorizontalScrollRef.value?.wrapRef) {
    elMenuHorizontalScrollRef.value.wrapRef.scrollLeft += eventDelta / 4;
  }
};

// 初始化数据，页面刷新时，滚动条滚动到对应位置
const initElMenuOffsetLeft = () => {
  nextTick(() => {
    let els: any = document.querySelector(".el-menu.el-menu--horizontal li.is-active");
    if (!els || !elMenuHorizontalScrollRef.value?.wrapRef) return false;
    elMenuHorizontalScrollRef.value.wrapRef.scrollLeft = els.offsetLeft;
  });
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

// 传送当前子级数据到菜单中
const setSendClassicChildren = (path: string) => {
  const currentPathSplit = path.split("/");
  let currentData: any = {};
  filterRoutesFun(routesList.routesList).forEach((v, k) => {
    if (v.path === `/${currentPathSplit[1]}`) {
      v["k"] = k;
      currentData["item"] = [{ ...v }];
      currentData["children"] = [{ ...v }];
      if (v.children) currentData["children"] = v.children;
    }
  });
  return currentData;
};

// 设置页面当前路由高亮
const setCurrentRouterHighlight = (currentRoute: any) => {
  const { path, meta } = currentRoute;
  if (theme.themeConfig.layout === "classic") {
    defaultActive.value = `/${path.split("/")[1]}`;
  } else {
    const pathSplit = meta?.isDynamic
      ? meta.isDynamicPath.split("/")
      : path.split("/");
    if (pathSplit.length >= 4 && meta?.isHide)
      defaultActive.value = pathSplit.slice(0, 3).join("/");
    else defaultActive.value = path;
  }
};

onBeforeMount(() => {
  setCurrentRouterHighlight(route);
});

onMounted(() => {
  initElMenuOffsetLeft();
});

// 路由更新时
onBeforeRouteUpdate((to) => {
  setCurrentRouterHighlight(to);
  proxy.mittBus.emit("onMenuClick");
  // 修复经典布局开启切割菜单时，点击tagsView后左侧导航菜单数据不变的问题
  let { layout, isClassicSplitMenu } = theme.themeConfig;
  if (layout === "classic" && isClassicSplitMenu) {
    proxy.mittBus.emit("setSendClassicChildren", setSendClassicChildren(to.path));
  }
});
</script>

<style scoped lang="scss">
.el-menu-horizontal-warp {
  flex: 1;
  overflow: hidden;
  margin-right: 30px;
  :deep(.el-scrollbar__bar.is-vertical) {
    display: none;
  }
  :deep(a) {
    width: 100%;
  }
  .el-menu.el-menu--horizontal {
    display: flex;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
  }
}
</style>
