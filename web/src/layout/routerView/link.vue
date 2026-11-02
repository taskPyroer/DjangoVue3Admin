<template>
  <div
    class="layout-view-bg-white flex layout-view-link"
    :style="{ height: `calc(100vh - ${setLinkHeight}` }"
  >
    <a :href="currentRouteMeta.isLink" target="_blank" rel="opener" class="flex-margin"
      >{{ $t(currentRouteMeta.title) }}：{{ currentRouteMeta.isLink }}</a
    >
  </div>
</template>

<script setup lang="ts" name="layoutLinkView">
import { ref, computed, watch } from "vue";
import { useRoute } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";

const route = useRoute();
const theme = useThemeConfigStateStore();
const currentRouteMeta = ref<any>({});

// 设置 link 的高度
const setLinkHeight = computed(() => {
  let { isTagsview } = theme.themeConfig;
  return isTagsview ? `114px` : `80px`;
});

// 监听路由的变化，设置内容
watch(
  () => route.path,
  () => {
    currentRouteMeta.value = route.meta;
  },
  {
    immediate: true,
  }
);
</script>
