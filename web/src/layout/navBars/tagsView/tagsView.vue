<template>
  <div
    class="layout-navbars-tagsview"
    :class="{ 'layout-navbars-tagsview-shadow': getThemeConfig.layout === 'classic' }"
  >
    <el-scrollbar ref="scrollbarRef" @wheel.prevent="onHandleScroll">
      <ul class="layout-navbars-tagsview-ul" :class="setTagsStyle" ref="tagsUlRef">
        <li
          v-for="(v, k) in tagsViewList"
          :key="k"
          class="layout-navbars-tagsview-ul-li"
          :data-url="v.url"
          :class="{ 'is-active': isActive(v) }"
          @contextmenu.prevent="onContextmenu(v, $event)"
          @click="onTagsClick(v, k)"
          :ref="
            (el) => {
              if (el) tagsRefs[k] = el;
            }
          "
        >
          <i
            class="iconfont icon-webicon318 layout-navbars-tagsview-ul-li-iconfont font14"
            v-if="isActive(v)"
          ></i>
          <SvgIcon
            :name="v.meta.icon"
            v-if="!isActive(v) && getThemeConfig.isTagsviewIcon"
            class="pr5"
          />
          <span>{{ $t(v.meta.title) }}</span>
          <template v-if="isActive(v)">
            <SvgIcon
              name="elementRefreshRight"
              :size="13"
              class="ml5 layout-navbars-tagsview-ul-li-refresh"
              @click.stop="refreshCurrentTagsView($route.fullPath)"
            />
            <SvgIcon
              name="elementClose"
              :size="13"
              class="layout-navbars-tagsview-ul-li-icon layout-icon-active"
              v-if="!v.meta.isAffix"
              @click.stop="
                closeCurrentTagsView(getThemeConfig.isShareTagsView ? v.path : v.url)
              "
            />
          </template>
          <SvgIcon
            name="elementClose"
            :size="13"
            class="layout-navbars-tagsview-ul-li-icon layout-icon-three"
            v-if="!v.meta.isAffix"
            @click.stop="
              closeCurrentTagsView(getThemeConfig.isShareTagsView ? v.path : v.url)
            "
          />
        </li>
      </ul>
    </el-scrollbar>
    <Contextmenu
      :dropdown="dropdown"
      ref="contextmenuRef"
      @currentContextmenuClick="onCurrentContextmenuClick"
    />
  </div>
</template>

<script setup lang="ts" name="layoutTagsView">
import {
  toRefs,
  reactive,
  onMounted,
  computed,
  ref,
  nextTick,
  onBeforeUpdate,
  onBeforeMount,
  onUnmounted,
  getCurrentInstance,
} from "vue";
import { useRoute, useRouter, onBeforeRouteUpdate } from "vue-router";
import Sortable from "sortablejs";
import { ElMessage } from "element-plus";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useTagsViewRoutesStore } from "@/stores/tagsViewRoutes";
import { Session } from "@/utils/storage";
import { isObjectValueEqual } from "@/utils/arrayOperation";
import Contextmenu from "@/layout/navBars/tagsView/contextmenu.vue";
import other from "@/utils/other";

const { proxy } = getCurrentInstance() as any;
const tagsRefs: any = ref([]);
const scrollbarRef = ref<any>(null);
const contextmenuRef = ref<any>(null);
const tagsUlRef = ref<any>(null);

const theme = useThemeConfigStateStore();
const tagsViewRoutes = useTagsViewRoutesStore();
const route = useRoute();
const router = useRouter();

const state: any = reactive({
  routeActive: "",
  routePath: route.path,
  dropdown: { x: 0, y: 0 },
  tagsRefsIndex: 0,
  tagsViewList: [],
  sortable: "",
  tagsViewRoutesList: [],
});

const { dropdown, tagsViewList } = toRefs(state);

// 动态设置 tagsView 风格样式
const setTagsStyle = computed(() => theme.themeConfig.tagsStyle);

// 获取布局配置信息
const getThemeConfig = computed(() => theme.themeConfig);

// 设置 tagsView 高亮
const isActive = (v: any) => {
  if (getThemeConfig.value.isShareTagsView) {
    return v.path === state.routePath;
  } else {
    return v.url ? v.url === state.routeActive : v.path === state.routeActive;
  }
};

// 存储 tagsViewList 到浏览器临时缓存中，页面刷新时，保留记录
const addBrowserSetSession = (tagsViewList: Array<object>) => {
  Session.set("tagsViewList", tagsViewList);
};

// 更新滚动条显示
const updateScrollbar = () => {
  scrollbarRef.value?.update?.();
};

// 鼠标滚轮滚动
const onHandleScroll = (e: any) => {
  if (scrollbarRef.value?.wrapRef) {
    scrollbarRef.value.wrapRef.scrollLeft += e.wheelDelta / 4;
  }
};

// tagsView 横向滚动
const tagsViewmoveToCurrentTag = () => {
  nextTick(() => {
    if (tagsRefs.value.length <= 0) return false;
    let liDom = tagsRefs.value[state.tagsRefsIndex];
    let liIndex = state.tagsRefsIndex;
    let liLength = tagsRefs.value.length;
    let liFirst: any = tagsRefs.value[0];
    let liLast: any = tagsRefs.value[tagsRefs.value.length - 1];
    let scrollRefs = scrollbarRef.value?.wrapRef;
    if (!scrollRefs) return;
    let scrollS = scrollRefs.scrollWidth;
    let offsetW = scrollRefs.offsetWidth;
    let scrollL = scrollRefs.scrollLeft;
    let liPrevTag: any = tagsRefs.value[state.tagsRefsIndex - 1];
    let liNextTag: any = tagsRefs.value[state.tagsRefsIndex + 1];
    let beforePrevL: any = "";
    let afterNextL: any = "";
    if (liDom === liFirst) {
      scrollRefs.scrollLeft = 0;
    } else if (liDom === liLast) {
      scrollRefs.scrollLeft = scrollS - offsetW;
    } else {
      if (liIndex === 0) beforePrevL = liFirst.offsetLeft - 5;
      else beforePrevL = liPrevTag?.offsetLeft - 5;
      if (liIndex === liLength)
        afterNextL = liLast.offsetLeft + liLast.offsetWidth + 5;
      else afterNextL = liNextTag.offsetLeft + liNextTag.offsetWidth + 5;
      if (afterNextL > scrollL + offsetW) {
        scrollRefs.scrollLeft = afterNextL - offsetW;
      } else if (beforePrevL < scrollL) {
        scrollRefs.scrollLeft = beforePrevL;
      }
    }
    updateScrollbar();
  });
};

// 获取 tagsView 的下标：用于处理 tagsView 点击时的横向滚动
const getTagsRefsIndex = (path: string) => {
  nextTick(async () => {
    let list = await state.tagsViewList;
    state.tagsRefsIndex = list.findIndex((v: any) => {
      if (getThemeConfig.value.isShareTagsView) {
        return v.path === path;
      } else {
        return v.url === path;
      }
    });
    tagsViewmoveToCurrentTag();
  });
};

// 处理 tagsView 高亮（多标签详情时使用，单标签详情未使用）
const setTagsViewHighlight = (v: any) => {
  let params = v.query && Object.keys(v.query).length > 0 ? v.query : v.params;
  if (!params || Object.keys(params).length <= 0) return v.path;
  let path = "";
  for (let i in params) {
    path += params[i];
  }
  return `${v.meta?.isDynamic ? v.meta.isDynamicPath : v.path}-${path}`;
};

// 处理可开启多标签详情，单标签详情（动态路由（xxx/:id/:name"），普通路由处理）
const solveAddTagsView = async (path: string, to?: any) => {
  let isDynamicPath = to.meta?.isDynamic ? to.meta.isDynamicPath : path;
  let current = state.tagsViewList.filter(
    (v: any) =>
      v.path === isDynamicPath &&
      isObjectValueEqual(
        to.meta?.isDynamic ? (v.params ? v.params : null) : v.query ? v.query : null,
        to.meta?.isDynamic
          ? to?.params
            ? to?.params
            : null
          : to?.query
          ? to?.query
          : null
      )
  );
  if (current.length <= 0) {
    let findItem = state.tagsViewRoutesList.find(
      (v: any) => v.path === isDynamicPath
    );
    if (!findItem) return false;
    if (findItem.meta?.isAffix) return false;
    if (findItem.meta?.isLink && !findItem.meta?.isIframe) return false;
    to.meta?.isDynamic ? (findItem.params = to.params) : (findItem.query = to.query);
    findItem.url = setTagsViewHighlight(findItem);
    state.tagsViewList.push({ ...findItem });
    addBrowserSetSession(state.tagsViewList);
  }
};

// 处理单标签时，第二次的值未覆盖第一次的 tagsViewList 值（Session Storage）
const singleAddTagsView = (path: string, to?: any) => {
  let isDynamicPath = to.meta?.isDynamic ? to.meta.isDynamicPath : path;
  state.tagsViewList.forEach((v: any) => {
    if (
      v.path === isDynamicPath &&
      !isObjectValueEqual(
        to.meta?.isDynamic ? (v.params ? v.params : null) : v.query ? v.query : null,
        to.meta?.isDynamic
          ? to?.params
            ? to?.params
            : null
          : to?.query
          ? to?.query
          : null
      )
    ) {
      to.meta?.isDynamic ? (v.params = to.params) : (v.query = to.query);
      v.url = setTagsViewHighlight(v);
      addBrowserSetSession(state.tagsViewList);
    }
  });
};

// 1、添加 tagsView
const addTagsView = (path: string, to?: any) => {
  nextTick(async () => {
    let item: any = "";
    if (to && to.meta?.isDynamic) {
      if (!getThemeConfig.value.isShareTagsView) await solveAddTagsView(path, to);
      else singleAddTagsView(path, to);
      if (state.tagsViewList.some((v: any) => v.path === to.meta.isDynamicPath))
        return false;
      item = state.tagsViewRoutesList.find(
        (v: any) => v.path === to.meta.isDynamicPath
      );
    } else {
      if (!getThemeConfig.value.isShareTagsView) await solveAddTagsView(path, to);
      else singleAddTagsView(path, to);
      if (state.tagsViewList.some((v: any) => v.path === path)) return false;
      item = state.tagsViewRoutesList.find((v: any) => v.path === path);
    }
    if (!item) return false;
    if (item.meta?.isLink && !item.meta?.isIframe) return false;
    if (to && to.meta?.isDynamic) item.params = to?.params ? to?.params : route.params;
    else item.query = to?.query ? to?.query : route.query;
    item.url = setTagsViewHighlight(item);
    state.tagsViewList.push({ ...item });
    addBrowserSetSession(state.tagsViewList);
  });
};

// 初始化 tagsView
const initTagsView = async () => {
  if (Session.get("tagsViewList") && getThemeConfig.value.isCacheTagsView) {
    state.tagsViewList = Session.get("tagsViewList");
  } else {
    state.tagsViewRoutesList.forEach((v: any) => {
      if (v.meta?.isAffix && !v.meta?.isHide) {
        v.url = setTagsViewHighlight(v);
        state.tagsViewList.push({ ...v });
      }
    });
    addTagsView(route.path, route);
  }
  getTagsRefsIndex(
    getThemeConfig.value.isShareTagsView ? state.routePath : state.routeActive
  );
};

// 获取 pinia 中的 tagsViewRoutes 列表
const getTagsViewRoutes = async () => {
  state.routeActive = setTagsViewHighlight(route);
  state.routePath = route.meta?.isDynamic
    ? route.meta.isDynamicPath
    : route.path;
  state.tagsViewList = [];
  state.tagsViewRoutesList = tagsViewRoutes.tagsViewRoutes;
  initTagsView();
};

// 2、刷新当前 tagsView
const refreshCurrentTagsView = (fullPath: string) => {
  proxy.mittBus.emit("onTagsViewRefreshRouterView", fullPath);
};

// 3、关闭当前 tagsView
const closeCurrentTagsView = (path: string) => {
  state.tagsViewList.forEach((v: any, k: number, arr: any) => {
    if (!v.meta?.isAffix) {
      if (getThemeConfig.value.isShareTagsView ? v.path === path : v.url === path) {
        state.tagsViewList.splice(k, 1);
        setTimeout(() => {
          if (
            state.tagsViewList.length === k && getThemeConfig.value.isShareTagsView
              ? state.routePath === path
              : state.routeActive === path
          ) {
            if (arr[arr.length - 1].meta?.isDynamic) {
              if (k !== arr.length)
                router.push({ name: arr[k].name, params: arr[k].params });
              else
                router.push({
                  name: arr[arr.length - 1].name,
                  params: arr[arr.length - 1].params,
                });
            } else {
              if (k !== arr.length)
                router.push({ path: arr[k].path, query: arr[k].query });
              else
                router.push({
                  path: arr[arr.length - 1].path,
                  query: arr[arr.length - 1].query,
                });
            }
          } else {
            if (
              state.tagsViewList.length !== k && getThemeConfig.value.isShareTagsView
                ? state.routePath === path
                : state.routeActive === path
            ) {
              if (arr[k].meta?.isDynamic) {
                router.push({ name: arr[k].name, params: arr[k].params });
              } else {
                router.push({ path: arr[k].path, query: arr[k].query });
              }
            }
          }
        }, 0);
      }
    }
  });
  addBrowserSetSession(state.tagsViewList);
};

// 4、关闭其它 tagsView
const closeOtherTagsView = (path: string) => {
  state.tagsViewList = [];
  state.tagsViewRoutesList.forEach((v: any) => {
    if (v.meta?.isAffix && !v.meta?.isHide) state.tagsViewList.push({ ...v });
  });
  addTagsView(path, route);
};

// 5、关闭全部 tagsView
const closeAllTagsView = () => {
  state.tagsViewList = [];
  state.tagsViewRoutesList.forEach((v: any) => {
    if (v.meta?.isAffix && !v.meta?.isHide) {
      state.tagsViewList.push({ ...v });
      router.push({ path: state.tagsViewList[state.tagsViewList.length - 1].path });
    }
  });
  addBrowserSetSession(state.tagsViewList);
};

// 6、开启当前页面全屏
const openCurrenFullscreen = async (path: string) => {
  const item = state.tagsViewList.find((v: any) =>
    getThemeConfig.value.isShareTagsView ? v.path === path : v.url === path
  );
  if (item) {
    if (item.meta?.isDynamic)
      await router.push({ name: item.name, params: item.params });
    else await router.push({ name: item.name, query: item.query });
    tagsViewRoutes.setCurrenFullscreen(true);
  }
};

const getCurrentRouteItem = (path: string, cParams: { [key: string]: any }) => {
  const itemRoute = Session.get("tagsViewList")
    ? Session.get("tagsViewList")
    : state.tagsViewList;
  return itemRoute.find((v: any) => {
    if (
      v.path === path &&
      isObjectValueEqual(
        v.meta?.isDynamic ? (v.params ? v.params : null) : v.query ? v.query : null,
        cParams && Object.keys(cParams ? cParams : {}).length > 0 ? cParams : null
      )
    ) {
      return v;
    } else if (v.path === path && Object.keys(cParams ? cParams : {}).length <= 0) {
      return v;
    }
  });
};

// 当前项右键菜单点击
const onCurrentContextmenuClick = async (item: any) => {
  const cParams = item.meta?.isDynamic ? item.params : item.query;
  const currentItem = getCurrentRouteItem(item.path, cParams);
  if (!currentItem)
    return ElMessage({
      type: "warning",
      message: "请正确输入路径及完整参数（query、params）",
    });
  const { path, name, params, query, meta, url } = currentItem;
  switch (item.contextMenuClickId) {
    case 0:
      if (meta?.isDynamic) await router.push({ name, params });
      else await router.push({ path, query });
      refreshCurrentTagsView(route.fullPath);
      break;
    case 1:
      closeCurrentTagsView(getThemeConfig.value.isShareTagsView ? path : url);
      break;
    case 2:
      if (meta?.isDynamic) await router.push({ name, params });
      else await router.push({ path, query });
      closeOtherTagsView(path);
      break;
    case 3:
      closeAllTagsView();
      break;
    case 4:
      openCurrenFullscreen(getThemeConfig.value.isShareTagsView ? path : url);
      break;
  }
};

// 右键点击时
const onContextmenu = (v: any, e: any) => {
  const { clientX, clientY } = e;
  state.dropdown.x = clientX;
  state.dropdown.y = clientY;
  contextmenuRef.value.openContextmenu(v);
};

// 当前的 tagsView 项点击时
const onTagsClick = (v: any, k: number) => {
  state.tagsRefsIndex = k;
  router.push(v);
};

// 设置 tagsView 可以进行拖拽
const initSortable = async () => {
  const el = document.querySelector(".layout-navbars-tagsview-ul") as HTMLElement;
  if (!el) return false;
  state.sortable?.el && state.sortable.destroy();
  state.sortable = Sortable.create(el, {
    animation: 300,
    dataIdAttr: "data-url",
    disabled: !getThemeConfig.value.isSortableTagsView,
    onEnd: () => {
      const sortEndList: any = [];
      state.sortable.toArray().forEach((val: any) => {
        state.tagsViewList.forEach((v: any) => {
          if (v.url === val) sortEndList.push({ ...v });
        });
      });
      addBrowserSetSession(sortEndList);
    },
  });
};

const onSortableResize = async () => {
  await initSortable();
  if (other.isMobile() && state.sortable?.el) state.sortable.destroy();
};

onBeforeMount(() => {
  onSortableResize();
  window.addEventListener("resize", onSortableResize);
  proxy.mittBus.on("onCurrentContextmenuClick", (data: object) => {
    onCurrentContextmenuClick(data);
  });
  proxy.mittBus.on("openOrCloseSortable", () => {
    initSortable();
  });
  proxy.mittBus.on("openShareTagsView", () => {
    if (getThemeConfig.value.isShareTagsView) {
      router.push("/home");
      state.tagsViewList = [];
      state.tagsViewRoutesList.forEach((v: any) => {
        if (v.meta?.isAffix && !v.meta?.isHide) {
          v.url = setTagsViewHighlight(v);
          state.tagsViewList.push({ ...v });
        }
      });
    }
  });
});

onUnmounted(() => {
  proxy.mittBus.off("onCurrentContextmenuClick");
  proxy.mittBus.off("openOrCloseSortable");
  proxy.mittBus.off("openShareTagsView");
  window.removeEventListener("resize", onSortableResize);
});

onBeforeUpdate(() => {
  tagsRefs.value = [];
});

onMounted(() => {
  getTagsViewRoutes();
  initSortable();
});

onBeforeRouteUpdate(async (to) => {
  state.routeActive = setTagsViewHighlight(to);
  state.routePath = to.meta?.isDynamic ? to.meta.isDynamicPath : to.path;
  await addTagsView(to.path, to);
  getTagsRefsIndex(
    getThemeConfig.value.isShareTagsView ? state.routePath : state.routeActive
  );
});

tagsViewRoutes.$subscribe((mutations, val) => {
  if (val.tagsViewRoutes.length === state.tagsViewRoutesList.length) return false;
  getTagsViewRoutes();
});
</script>

<style scoped lang="scss">
.layout-navbars-tagsview {
  background-color: var(--el-color-white);
  border-bottom: 1px solid #f1f2f3;
  z-index: 4;
  position: relative;
  :deep(.el-scrollbar__wrap) {
    overflow-x: auto !important;
  }
  &-ul {
    list-style: none;
    margin: 0;
    padding: 0;
    height: 34px;
    display: flex;
    align-items: center;
    color: var(--el-text-color-regular);
    font-size: 12px;
    white-space: nowrap;
    padding: 0 15px;
    &-li {
      height: 26px;
      line-height: 26px;
      display: flex;
      align-items: center;
      border: 1px solid #e6e6e6;
      padding: 0 15px;
      margin-right: 5px;
      border-radius: 2px;
      position: relative;
      z-index: 0;
      cursor: pointer;
      justify-content: space-between;
      &:hover {
        background-color: var(--color-primary-light-9);
        color: var(--color-primary);
        border-color: var(--color-primary-light-6);
      }
      &-iconfont {
        position: relative;
        left: -5px;
        font-size: 12px;
      }
      &-icon {
        border-radius: 100%;
        position: relative;
        height: 14px;
        width: 14px;
        text-align: center;
        line-height: 14px;
        right: -5px;
        &:hover {
          color: var(--color-whites);
          background-color: var(--color-primary-light-3);
        }
      }
      .layout-icon-active {
        display: block;
      }
      .layout-icon-three {
        display: none;
      }
    }
    .is-active {
      color: var(--color-whites);
      background: var(--color-primary);
      border-color: var(--color-primary);
      transition: border-color 3s ease;
    }
  }
  // 风格2
  .tags-style-two {
    .layout-navbars-tagsview-ul-li {
      height: 34px !important;
      line-height: 34px !important;
      border: none !important;
      .layout-navbars-tagsview-ul-li-iconfont {
        display: none;
      }
      .layout-icon-active {
        display: none;
      }
      .layout-icon-three {
        display: block;
      }
    }
    .is-active {
      background: none !important;
      color: var(--color-primary) !important;
      border-bottom: 2px solid !important;
      border-color: var(--color-primary) !important;
      border-radius: 0 !important;
    }
  }
  // 风格3
  .tags-style-three {
    .layout-navbars-tagsview-ul-li {
      height: 34px !important;
      line-height: 34px !important;
      border-right: 1px solid #f6f6f6 !important;
      border-top: none !important;
      border-bottom: none !important;
      border-left: none !important;
      border-radius: 0 !important;
      margin-right: 0 !important;
      &:first-of-type {
        border-left: 1px solid #f6f6f6 !important;
      }
      .layout-icon-active {
        display: none;
      }
      .layout-icon-three {
        display: block;
      }
    }
    .is-active {
      background: var(--el-color-white) !important;
      color: var(--color-primary) !important;
      border-top: 1px solid !important;
      border-top-color: var(--color-primary) !important;
    }
  }
  // 风格4
  .tags-style-four {
    .layout-navbars-tagsview-ul-li {
      margin-right: 0 !important;
      border: none !important;
      position: relative;
      border-radius: 3px !important;
      .layout-icon-active {
        display: none;
      }
      .layout-icon-three {
        display: block;
      }
      &:hover {
        background: none !important;
      }
    }
    .is-active {
      background: none !important;
      color: var(--color-primary) !important;
    }
  }
  .tags-style-five {
    align-items: flex-end;
    .tags-style-five-svg {
      -webkit-mask-box-image: url("data:image/svg+xml,%3Csvg width='68' height='34' viewBox='0 0 68 34' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill-rule='evenodd' clip-rule='evenodd' d='m27,0c-7.99582,0 -11.95105,0.00205 -12,12l0,6c0,8.284 -0.48549,16.49691 -8.76949,16.49691l54.37857,-0.11145c-8.284,0 -8.60908,-8.10146 -8.60908,-16.38546l0,-6c0.11145,-12.08445 -4.38441,-12 -12,-12l-13,0z' fill='%23409eff'/%3E%3C/svg%3E")
        12 27 15;
    }
    .layout-navbars-tagsview-ul-li {
      padding: 0 5px;
      border-width: 15px 27px 15px;
      border-style: solid;
      border-color: transparent;
      margin: 0 -15px;
      .layout-icon-active,
      .layout-navbars-tagsview-ul-li-iconfont,
      .layout-navbars-tagsview-ul-li-refresh {
        display: none;
      }
      .layout-icon-three {
        display: block;
      }
      &:hover {
        @extend .tags-style-five-svg;
        background: var(--color-primary-light-9);
      }
    }
    .is-active {
      @extend .tags-style-five-svg;
      background: var(--color-primary) !important;
      z-index: 1;
    }
  }
}
.layout-navbars-tagsview-shadow {
  box-shadow: rgb(0 21 41 / 4%) 0px 1px 4px;
}
</style>
