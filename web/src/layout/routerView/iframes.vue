<template>
  <div
    class="layout-view-bg-white flex mt1"
    :style="{ height: `calc(100vh - ${setIframeHeight}`, border: 'none' }"
    v-loading="iframeLoading"
  >
    <iframe
      :src="iframeUrl"
      frameborder="0"
      height="100%"
      width="100%"
      id="iframe"
      v-show="!iframeLoading"
    ></iframe>
  </div>
</template>

<script setup lang="ts" name="layoutIfameView">
import {
  ref,
  onMounted,
  nextTick,
  watch,
  computed,
} from "vue";
import { useRoute } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useTagsViewRoutesStore } from "@/stores/tagsViewRoutes";

const route = useRoute();
const theme = useThemeConfigStateStore();
const tagsViewRoutes = useTagsViewRoutesStore();

const iframeLoading = ref(true);
const iframeUrl = ref<any>("");

// 初始化页面加载 loading
const initIframeLoad = () => {
  iframeUrl.value = route.meta.isLink;
  nextTick(() => {
    iframeLoading.value = true;
    const iframe = document.getElementById("iframe");
    if (!iframe) return false;
    iframe.onload = () => {
      iframeLoading.value = false;
    };
  });
};

// 设置 iframe 的高度
const setIframeHeight = computed(() => {
  let { isTagsview } = theme.themeConfig;
  let { isTagsViewCurrenFull } = tagsViewRoutes;
  if (isTagsViewCurrenFull) {
    return `1px`;
  } else {
    return isTagsview ? `85px` : `51px`;
  }
});

onMounted(() => {
  initIframeLoad();
});

// 监听路由变化，多个 iframe 时使用
watch(
  () => route.path,
  () => {
    initIframeLoad();
  }
);
</script>
