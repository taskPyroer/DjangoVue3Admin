<template>
  <el-container class="layout-container">
    <Aside />
    <el-container class="flex-center" :class="{ 'layout-backtop': !isFixedHeader }">
      <Header v-if="isFixedHeader" />
      <el-scrollbar
        ref="layoutDefaultsScrollbarRef"
        :class="{ 'layout-backtop': isFixedHeader }"
      >
        <Header v-if="!isFixedHeader" />
        <Main />
      </el-scrollbar>
    </el-container>
    <el-backtop target=".layout-backtop .el-scrollbar__wrap"></el-backtop>
  </el-container>
</template>

<script setup lang="ts" name="layoutDefaults">
import { computed, watch, ref } from "vue";
import { useRoute } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import Aside from "@/layout/component/aside.vue";
import Header from "@/layout/component/header.vue";
import Main from "@/layout/component/main.vue";

const route = useRoute();
const theme = useThemeConfigStateStore();
const layoutDefaultsScrollbarRef = ref<any>(null);

const isFixedHeader = computed(() => theme.themeConfig.isFixedHeader);

// 监听路由的变化
watch(
  () => route.path,
  () => {
    if (layoutDefaultsScrollbarRef.value) {
      if (layoutDefaultsScrollbarRef.value.setScrollTop) {
        layoutDefaultsScrollbarRef.value.setScrollTop(0);
      } else if (layoutDefaultsScrollbarRef.value.wrapRef) {
        layoutDefaultsScrollbarRef.value.wrapRef.scrollTop = 0;
      }
    }
  }
);
</script>
