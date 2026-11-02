<template>
	<el-container class="layout-container flex-center">
		<Header />
		<el-container class="layout-mian-height-50">
			<Aside />
			<div class="flex-center layout-backtop">
				<TagsView v-if="getThemeConfig.isTagsview" />
				<Main />
			</div>
		</el-container>
		<el-backtop target=".layout-backtop .el-main .el-scrollbar__wrap"></el-backtop>
	</el-container>
</template>

<script setup lang="ts" name="layoutClassic">
import { computed } from 'vue';
import { useThemeConfigStateStore } from '@/stores/themeConfig';
import Aside from '@/layout/component/aside.vue';
import Header from '@/layout/component/header.vue';
import Main from '@/layout/component/main.vue';
import TagsView from '@/layout/navBars/tagsView/tagsView.vue';

const theme = useThemeConfigStateStore();
const getThemeConfig = computed(() => theme.themeConfig);
</script>
