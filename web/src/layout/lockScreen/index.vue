<template>
	<div v-show="isShowLockScreen">
		<div class="layout-lock-screen-img" :class="{ 'layout-lock-screen-filter': isShowLoockLogin }"></div>
		<div class="layout-lock-screen">
			<div
				class="layout-lock-screen-date"
				ref="layoutLockScreenDateRef"
				@mousedown="onDown"
				@mousemove="onMove"
				@mouseup="onEnd"
				@touchstart.stop="onDown"
				@touchmove.stop="onMove"
				@touchend.stop="onEnd"
			>
				<div class="layout-lock-screen-date-box">
					<div class="layout-lock-screen-date-box-time">
						{{ time.hm }}<span class="layout-lock-screen-date-box-minutes">{{ time.s }}</span>
					</div>
					<div class="layout-lock-screen-date-box-info">{{ time.mdq }}</div>
				</div>
				<div class="layout-lock-screen-date-top">
					<SvgIcon name="elementTop" />
					<div class="layout-lock-screen-date-top-text">上滑解锁</div>
				</div>
			</div>
			<transition name="el-zoom-in-center">
				<div v-show="isShowLoockLogin" class="layout-lock-screen-login">
					<div class="layout-lock-screen-login-box">
						<div class="layout-lock-screen-login-box-img">
							<img :src="rotate" />
						</div>
						<div class="layout-lock-screen-login-box-name">DjangoAdmin</div>
						<div class="layout-lock-screen-login-box-value">
							<el-input
								placeholder="请输入密码"
								ref="layoutLockScreenInputRef"
								v-model="lockScreenPassword"
								@keyup.enter.stop="onLockScreenSubmit()"
							>
								<template #append>
									<el-button @click="onLockScreenSubmit">
										<el-icon class="el-input__icon">
											<elementRight />
										</el-icon>
									</el-button>
								</template>
							</el-input>
						</div>
					</div>
					<div class="layout-lock-screen-login-icon">
						<SvgIcon name="elementMicrophone" />
						<SvgIcon name="elementAlarmClock" />
						<SvgIcon name="elementSwitchButton" />
					</div>
				</div>
			</transition>
		</div>
	</div>
</template>

<script setup lang="ts" name="layoutLockScreen">
import { onMounted, reactive, toRefs, ref, onUnmounted } from 'vue';
import { useThemeConfigStateStore } from '@/stores/themeConfig';
import { formatDate } from '@/utils/formatTime';
import { Local } from '@/utils/storage';
import rotate from '@/assets/rotate.png';

const layoutLockScreenInputRef = ref<any>(null);
const layoutLockScreenDateRef = ref<any>(null);
const theme = useThemeConfigStateStore();

const state: any = reactive({
	transparency: 1,
	downClientY: 0,
	moveDifference: 0,
	isShowLoockLogin: false,
	isFlags: false,
	time: {
		hm: '',
		s: '',
		mdq: '',
	},
	setIntervalTime: 0,
	isShowLockScreen: false,
	isShowLockScreenIntervalTime: 0,
	lockScreenPassword: '',
});

const {
	isShowLoockLogin,
	time,
	isShowLockScreen,
	lockScreenPassword,
} = toRefs(state);

// 鼠标按下
const onDown = (down: any) => {
	state.isFlags = true;
	state.downClientY = down.touches ? down.touches[0].clientY : down.clientY;
};

// 鼠标移动
const onMove = (move: any) => {
	if (state.isFlags && layoutLockScreenDateRef.value) {
		const el = layoutLockScreenDateRef.value;
		const opacitys = (state.transparency -= 1 / 200);
		if (move.touches) {
			state.moveDifference = move.touches[0].clientY - state.downClientY;
		} else {
			state.moveDifference = move.clientY - state.downClientY;
		}
		if (state.moveDifference >= 0) return false;
		el.setAttribute('style', `top:${state.moveDifference}px;cursor:pointer;opacity:${opacitys};`);
		if (state.moveDifference < -400) {
			el.setAttribute('style', `top:${-el.clientHeight}px;cursor:pointer;transition:all 0.3s ease;`);
			state.moveDifference = -el.clientHeight;
			setTimeout(() => {
				el && el.parentNode?.removeChild(el);
			}, 300);
		}
		if (state.moveDifference === -el.clientHeight) {
			state.isShowLoockLogin = true;
			layoutLockScreenInputRef.value?.focus?.();
		}
	}
};

// 鼠标松开
const onEnd = () => {
	state.isFlags = false;
	state.transparency = 1;
	if (state.moveDifference >= -400 && layoutLockScreenDateRef.value) {
		layoutLockScreenDateRef.value.setAttribute('style', `top:0px;opacity:1;transition:all 0.3s ease;`);
	}
};

// 时间初始化
const initTime = () => {
	state.time.hm = formatDate(new Date(), 'HH:MM');
	state.time.s = formatDate(new Date(), 'SS');
	state.time.mdq = formatDate(new Date(), 'mm月dd日，WWW');
};

// 时间初始化定时器
const initSetTime = () => {
	initTime();
	state.setIntervalTime = window.setInterval(() => {
		initTime();
	}, 1000);
};

// 存储布局配置
const setLocalThemeConfig = () => {
	theme.themeConfig.isDrawer = false;
	Local.set('themeConfig', theme.themeConfig);
};

// 锁屏时间定时器
const initLockScreen = () => {
	if (theme.themeConfig.isLockScreen) {
		state.isShowLockScreenIntervalTime = window.setInterval(() => {
			if (theme.themeConfig.lockScreenTime <= 1) {
				state.isShowLockScreen = true;
				setLocalThemeConfig();
				return false;
			}
			theme.themeConfig.lockScreenTime--;
		}, 1000);
	} else {
		clearInterval(state.isShowLockScreenIntervalTime);
	}
};

// 密码输入点击事件
const onLockScreenSubmit = () => {
	theme.themeConfig.isLockScreen = false;
	theme.themeConfig.lockScreenTime = 30;
	setLocalThemeConfig();
};

onMounted(() => {
	initSetTime();
	initLockScreen();
});

onUnmounted(() => {
	window.clearInterval(state.setIntervalTime);
	window.clearInterval(state.isShowLockScreenIntervalTime);
});
</script>

<style scoped lang="scss">
.layout-lock-screen-fixed {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
}
.layout-lock-screen-filter {
	filter: blur(1px);
}
.layout-lock-screen-img {
	@extend .layout-lock-screen-fixed;
	background-image: url('@/assets/lock.jpg');
	background-size: 100% 100%;
	z-index: 999;
}
.layout-lock-screen {
	@extend .layout-lock-screen-fixed;
	z-index: 9999992;
	&-date {
		position: absolute;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		color: var(--color-whites);
		z-index: 1000;
		user-select: none;
		&-box {
			position: absolute;
			left: 30px;
			bottom: 50px;
			&-time {
				font-size: 100px;
				color: var(--color-whites);
			}
			&-info {
				font-size: 40px;
				color: var(--color-whites);
			}
			&-minutes {
				font-size: 16px;
			}
		}
		&-top {
			position: absolute;
			left: 50%;
			bottom: 30px;
			transform: translateX(-50%);
			text-align: center;
			color: var(--color-whites);
			&-text {
				font-size: 12px;
			}
			i {
				transform: translateY(0px);
				animation: error-num 1s linear infinite;
			}
		}
	}
	&-login {
		position: relative;
		z-index: 1024;
		width: 100%;
		height: 100%;
		left: 0;
		top: 0;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		&-box {
			text-align: center;
			margin: auto;
			&-img {
				width: 180px;
				height: 180px;
				margin: auto;
				img {
					width: 100%;
					height: 100%;
					border-radius: 100%;
				}
			}
			&-name {
				font-size: 26px;
				margin: 15px 0 30px;
				color: #fff;
			}
		}
		&-icon {
			position: absolute;
			right: 30px;
			bottom: 30px;
			i {
				font-size: 20px;
				margin-left: 15px;
				cursor: pointer;
				color: #fff;
				opacity: 0.8;
				&:hover {
					opacity: 1;
				}
			}
		}
	}
}
</style>
