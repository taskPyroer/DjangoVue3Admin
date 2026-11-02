<template>
	<div class="layout-footer mt15" v-show="isDelayFooter">
		<div class="layout-footer-warp">
			<div>PaoPao-Admin，Made by PaoPao with ❤️</div>
			<div class="mt5">{{ $t('message.copyright.one5') }}</div>
		</div>
	</div>
</template>

<script setup lang="ts" name="layoutFooter">
import { ref } from 'vue';
import { onBeforeRouteUpdate } from 'vue-router';

const isDelayFooter = ref(true);

// 路由改变时，等主界面动画加载完毕再显示 footer
onBeforeRouteUpdate(() => {
	isDelayFooter.value = false;
	setTimeout(() => {
		isDelayFooter.value = true;
	}, 800);
});
</script>

<style scoped lang="scss">
.layout-footer {
	width: 100%;
	display: flex;
	&-warp {
		margin: auto;
		color: var(--el-text-color-secondary);
		text-align: center;
		animation: logoAnimation 0.3s ease-in-out;
	}
}
</style>
