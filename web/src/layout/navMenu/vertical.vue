<template>
  <el-menu
    router
    :default-active="defaultActive"
    background-color="transparent"
    :collapse="isCollapse"
    :unique-opened="getThemeConfig.isUniqueOpened"
    :collapse-transition="false"
  >
    <template v-for="val in menuLists">
      <el-sub-menu
        :index="val.path"
        v-if="val.children && val.children.length > 0"
        :key="val.path"
      >
        <template #title>
          <SvgIcon :name="val.meta.icon"/>
          <span>{{ $t(val.meta.title) }}</span>
        </template>
        <SubItem :chil="val.children" />
      </el-sub-menu>
      <el-menu-item :index="val.path" :key="val.path" v-else>
        <SvgIcon :name="val.meta.icon" />
        <template
          #title
          v-if="!val.meta.isLink || (val.meta.isLink && val.meta.isIframe)"
        >
          <span>{{ $t(val.meta.title) }}</span>
        </template>
        <template #title v-else>
          <a :href="val.meta.isLink" target="_blank" rel="opener">{{
            $t(val.meta.title)
          }}</a>
        </template>
      </el-menu-item>
    </template>
  </el-menu>
</template>

<script setup lang="ts" name="navMenuVertical">
import {
  ref,
  computed,
  getCurrentInstance,
  onMounted,
  watch,
} from "vue";
import { useRoute, onBeforeRouteUpdate } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
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
const theme = useThemeConfigStateStore();
const route = useRoute();

const defaultActive = ref<any>(
  route.meta?.isDynamic ? route.meta?.isDynamicPath : route.path
);
const isCollapse = ref(false);

// 获取父级菜单数据
const menuLists = computed(() => props.menuList);

// 获取布局配置信息
const getThemeConfig = computed(() => theme.themeConfig);

// 菜单高亮（详情时，父级高亮）
const setParentHighlight = (currentRoute: any) => {
  const { path, meta } = currentRoute;
  const pathSplit = meta?.isDynamic ? meta.isDynamicPath.split("/") : path.split("/");
  if (pathSplit.length >= 4 && meta?.isHide) return pathSplit.slice(0, 3).join("/");
  return path;
};

// 设置菜单的收起/展开
watch(
  () => theme.themeConfig.isCollapse,
  () => {
    isCollapse.value =
      document.body.clientWidth <= 1000 ? false : !!getThemeConfig.value.isCollapse;
  },
  {
    immediate: true,
  }
);

onMounted(() => {
  defaultActive.value = setParentHighlight(route);
});

// 路由更新时
onBeforeRouteUpdate((to) => {
  defaultActive.value = setParentHighlight(to);
  proxy.mittBus.emit("onMenuClick");
  if (document.body.clientWidth < 1000) {
    getThemeConfig.value.isCollapse = false;
  }
});
</script>
