<template>
	<transition name="el-zoom-in-center">
		<div
			aria-hidden="true"
			class="el-dropdown__popper el-popper is-light is-pure custom-contextmenu"
			role="tooltip"
			data-popper-placement="bottom"
			:style="`top: ${dropdowns.y + 5}px;left: ${dropdowns.x}px;`"
			v-show="isShow"
		>
			<ul class="el-dropdown-menu">
				<template v-for="(v, k) in dropdownList">
					<li
						class="el-dropdown-menu__item"
						aria-disabled="false"
						tabindex="-1"
						:key="k"
						v-if="!v.affix"
						@click="onCurrentContextmenuClick(v.contextMenuClickId)"
					>
						<SvgIcon :name="v.icon" />
						<span>{{ $t(v.txt) }}</span>
					</li>
				</template>
			</ul>
			<div class="el-popper__arrow" :style="{ left: `${arrowLeft}px` }"></div>
		</div>
	</transition>
</template>

<script setup lang="ts" name="layoutTagsViewContextmenu">
import { ref, computed, reactive, onMounted, onUnmounted, watch } from 'vue';

const props = withDefaults(
	defineProps<{
		dropdown?: any;
	}>(),
	{
		dropdown: () => ({ x: 0, y: 0 }),
	}
);

const emit = defineEmits<{
	(e: 'currentContextmenuClick', data: any): void;
}>();

const isShow = ref(false);
const arrowLeft = ref(10);
const item = ref<any>({});
const dropdownList = reactive([
	{ contextMenuClickId: 0, txt: 'message.tagsView.refresh', affix: false, icon: 'elementRefreshRight' },
	{ contextMenuClickId: 1, txt: 'message.tagsView.close', affix: false, icon: 'elementClose' },
	{ contextMenuClickId: 2, txt: 'message.tagsView.closeOther', affix: false, icon: 'elementCircleClose' },
	{ contextMenuClickId: 3, txt: 'message.tagsView.closeAll', affix: false, icon: 'elementFolderDelete' },
	{
		contextMenuClickId: 4,
		txt: 'message.tagsView.fullscreen',
		affix: false,
		icon: 'iconfont icon-fullscreen',
	},
]);

// 父级传过来的坐标 x,y 值
const dropdowns = computed(() => {
	if (props.dropdown.x + 117 > document.documentElement.clientWidth) {
		return {
			x: document.documentElement.clientWidth - 117 - 5,
			y: props.dropdown.y,
		};
	} else {
		return props.dropdown;
	}
});

// 当前项菜单点击
const onCurrentContextmenuClick = (contextMenuClickId: number) => {
	emit('currentContextmenuClick', Object.assign({}, { contextMenuClickId }, item.value));
};

// 打开右键菜单：判断是否固定，固定则不显示关闭按钮
const openContextmenu = (menuItem: any) => {
	item.value = menuItem;
	dropdownList[1].affix = !!menuItem.meta?.isAffix;
	closeContextmenu();
	setTimeout(() => {
		isShow.value = true;
	}, 10);
};

// 关闭右键菜单
const closeContextmenu = () => {
	isShow.value = false;
};

// 监听下拉菜单位置
watch(
	() => props.dropdown,
	({ x }) => {
		if (x + 117 > document.documentElement.clientWidth) arrowLeft.value = 117 - (document.documentElement.clientWidth - x);
		else arrowLeft.value = 10;
	},
	{
		deep: true,
	}
);

onMounted(() => {
	document.body.addEventListener('click', closeContextmenu);
});

onUnmounted(() => {
	document.body.removeEventListener('click', closeContextmenu);
});

defineExpose({
	openContextmenu,
});
</script>

<style scoped lang="scss">
.custom-contextmenu {
	transform-origin: center top;
	z-index: 2190;
	position: fixed;
	.el-dropdown-menu__item {
		font-size: 12px !important;
		white-space: nowrap;
		i {
			font-size: 12px !important;
		}
	}
}
.el-dropdown-menu-arrow {
	&::before {
		content: '';
	}
}
</style>
