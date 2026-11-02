<template>
  <div class="h100">
    <router-view v-slot="{ Component }">
      <transition :name="setTransitionName" mode="out-in">
        <keep-alive :include="keepAliveNameList">
          <component :is="Component" :key="refreshRouterViewKey" class="w100" />
        </keep-alive>
      </transition>
    </router-view>
  </div>
</template>

<script setup lang="ts" name="layoutParentView">
import {
  computed,
  toRefs,
  reactive,
  getCurrentInstance,
  onBeforeMount,
  onUnmounted,
  nextTick,
  watch,
} from "vue";
import { useRoute } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useKeepAliveNamesStore } from "@/stores/keepAliveNames";

const { proxy } = getCurrentInstance() as any;
const route = useRoute();
const theme = useThemeConfigStateStore();
const keepAliveNames = useKeepAliveNamesStore();

const state: any = reactive({
  refreshRouterViewKey: null,
  keepAliveNameList: [],
});

const { refreshRouterViewKey, keepAliveNameList } = toRefs(state);

// 设置主界面切换动画
const setTransitionName = computed(() => theme.themeConfig.animation);

// 获取布局配置信息
const getThemeConfig = computed(() => theme.themeConfig);

// 获取组件缓存列表(name值)
const getKeepAliveNames = computed(() => keepAliveNames.keepAliveNames);

onBeforeMount(() => {
  state.keepAliveNameList = getKeepAliveNames.value;
  proxy.mittBus.on("onTagsViewRefreshRouterView", (fullPath: string) => {
    state.keepAliveNameList = getKeepAliveNames.value.filter(
      (name: string) => route.name !== name
    );
    state.refreshRouterViewKey = null;
    nextTick(() => {
      state.refreshRouterViewKey = fullPath;
      state.keepAliveNameList = getKeepAliveNames.value;
    });
  });
});

onUnmounted(() => {
  proxy.mittBus.off("onTagsViewRefreshRouterView");
});

// 监听路由变化，防止 tagsView 多标签时，切换动画消失
watch(
  () => route.fullPath,
  () => {
    state.refreshRouterViewKey = route.fullPath;
  }
);
</script>
