<template>
  <div class="el-menu-horizontal-warp">
    <el-scrollbar
      @wheel.native.prevent="onElMenuHorizontalScroll"
      ref="elMenuHorizontalScrollRef"
    >
      <el-menu
        router
        :default-active="defaultActive"
        :ellipsis="false"
        background-color="transparent"
        mode="horizontal"
      >
        <template v-for="val in menuLists">
          <el-sub-menu
            :index="val.path"
            v-if="val.children && val.children.length > 0"
            :key="val.path"
          >
            <template #title>
              <SvgIcon :name="val.meta.icon" />
              {{ $t(val.meta.title) }}
            </template>
            <SubItem :chil="val.children" />
          </el-sub-menu>
          <el-menu-item :index="val.path" :key="val.path" v-else>
            <template
              #title
              v-if="!val.meta.isLink || (val.meta.isLink && val.meta.isIframe)"
            >
              <SvgIcon :name="val.meta.icon" />
              {{ $t(val.meta.title) }}
            </template>
            <template #title v-else>
              <a :href="val.meta.isLink" target="_blank" rel="opener">
                <SvgIcon :name="val.meta.icon" />
                {{ $t(val.meta.title) }}
              </a>
            </template>
          </el-menu-item>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>
</template>

<script lang="ts">
import {
  toRefs,
  reactive,
  computed,
  defineComponent,
  getCurrentInstance,
  onMounted,
  nextTick,
  onBeforeMount,
  ref
} from "vue";
import { useRoute, onBeforeRouteUpdate } from "vue-router";
import { useThemeConfigStateStore } from "@/stores/themeConfig";
import { useRoutesListStore } from "@/stores/routesList";
import SubItem from "@/layout/navMenu/subItem.vue";
export default defineComponent({
  name: "navMenuHorizontal",
  components: { SubItem },
  props: {
    menuList: {
      type: Array,
      default: () => [],
    },
  },
  setup(props) {
    const { proxy } = getCurrentInstance() as any;
    const route = useRoute();

    const theme = useThemeConfigStateStore();
    const routesList = useRoutesListStore();
    const state: any = reactive({
      defaultActive: null,
    });
    // 获取父级菜单数据
    const menuLists = computed(() => {
      return props.menuList;
    });
    // 设置横向滚动条可以鼠标滚轮滚动
    const onElMenuHorizontalScroll = (e: any) => {
      const eventDelta = e.wheelDelta || -e.deltaY * 40;
      proxy.$refs.elMenuHorizontalScrollRef.$refs.wrapRef.scrollLeft =
        proxy.$refs.elMenuHorizontalScrollRef.$refs.wrapRef.scrollLeft + eventDelta / 4;
    };
    // 初始化数据，页面刷新时，滚动条滚动到对应位置
    const initElMenuOffsetLeft = () => {
      nextTick(() => {
        let els: any = document.querySelector('.el-menu.el-menu--horizontal li.is-active');
        if (!els) return false;
        proxy.$refs.elMenuHorizontalScrollRef.$refs.wrapRef.scrollLeft = els.offsetLeft;
      });
    };

    // 路由过滤递归函数
    const filterRoutesFun = (arr: Array<object>) => {
      return arr
        .filter((item: any) => !item.meta.isHide)
        .map((item: any) => {
          item = Object.assign({}, item);
          if (item.children) item.children = filterRoutesFun(item.children);
          return item;
        });
    };
    // 传送当前子级数据到菜单中
    const setSendClassicChildren = (path: string) => {
      const currentPathSplit = path.split("/");
      let currentData: any = {};
      filterRoutesFun(routesList.routesList).map((v, k) => {
        if (v.path === `/${currentPathSplit[1]}`) {
          v["k"] = k;
          currentData["item"] = [{ ...v }];
          currentData["children"] = [{ ...v }];
          if (v.children) currentData["children"] = v.children;
        }
      });
      return currentData;
    };
    // 设置页面当前路由高亮
    const setCurrentRouterHighlight = (currentRoute:any) => {
      const { path, meta } = currentRoute;
      if (theme.themeConfig.layout === "classic") {
        state.defaultActive = `/${path.split("/")[1]}`;
      } else {
        const pathSplit = meta.isDynamic
          ? meta.isDynamicPath.split("/")
          : path.split("/");
        if (pathSplit.length >= 4 && meta.isHide)
          state.defaultActive = pathSplit.splice(0, 3).join("/");
        else state.defaultActive = path;
      }
    };
    // 页面加载前
    onBeforeMount(() => {
      setCurrentRouterHighlight(route);
    });
    // 页面加载时
    onMounted(() => {
      initElMenuOffsetLeft();
    });
    // 路由更新时
    onBeforeRouteUpdate((to) => {
      // 修复
      setCurrentRouterHighlight(to);
      proxy.mittBus.emit("onMenuClick");
      // 修复经典布局开启切割菜单时，点击tagsView后左侧导航菜单数据不变的问题
      let { layout, isClassicSplitMenu } = theme.themeConfig;
      if (layout === "classic" && isClassicSplitMenu) {
        proxy.mittBus.emit("setSendClassicChildren", setSendClassicChildren(to.path));
      }
    });
    return {
      menuLists,
      onElMenuHorizontalScroll,
      ...toRefs(state),
    };
  },
});
</script>

<style scoped lang="scss">
.el-menu-horizontal-warp {
  flex: 1;
  overflow: hidden;
  margin-right: 30px;
  ::v-deep(.el-scrollbar__bar.is-vertical) {
    display: none;
  }
  ::v-deep(a) {
    width: 100%;
  }
 .el-menu.el-menu--horizontal {
    display: flex;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
  }
}
</style>
