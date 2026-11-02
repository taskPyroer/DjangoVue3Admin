<template>
  <el-header
    class="layout-header"
    :height="setHeaderHeight"
    v-show="!isTagsViewCurrenFull"
  >
    <NavBarsIndex />
  </el-header>
</template>

<script setup lang="ts" name="layoutHeader">
import { computed } from "vue";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useTagsViewRoutesStore } from "@/stores/tagsViewRoutes";
import NavBarsIndex from "@/layout/navBars/index.vue";

const theme = useThemeConfigStateStore();
const tagsViewRoutes = useTagsViewRoutesStore();

// 设置 header 的高度
const setHeaderHeight = computed(() => {
  let { isTagsview, layout } = theme.themeConfig;
  return isTagsview && layout !== "classic" ? "84px" : "50px";
});

// 获取卡片全屏信息
const isTagsViewCurrenFull = computed(() => tagsViewRoutes.isTagsViewCurrenFull);
</script>
