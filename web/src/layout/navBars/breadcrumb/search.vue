<template>
  <div class="layout-search-dialog">
    <el-dialog v-model="isShowSearch" destroy-on-close :show-close="false">
      <template #footer>
        <el-autocomplete
          v-model="menuQuery"
          :fetch-suggestions="menuSearch"
          :placeholder="$t('message.user.searchPlaceholder')"
          ref="layoutMenuAutocompleteRef"
          @select="onHandleSelect"
          :fit-input-width="true"
        >
          <template #prefix>
            <el-icon class="el-input__icon">
              <elementSearch />
            </el-icon>
          </template>
          <template #default="{ item }">
            <div>
              <SvgIcon :name="item.meta.icon" class="mr5" />
              {{ $t(item.meta.title) }}
            </div>
          </template>
        </el-autocomplete>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="layoutBreadcrumbSearch">
import { ref, reactive, toRefs, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { storeToRefs } from 'pinia';
import { useTagsViewRoutesStore } from '@/stores/tagsViewRoutes';

interface SearchState {
  isShowSearch: boolean;
  menuQuery: string;
  tagsViewList: object[];
}

interface Restaurant {
  path: string;
  meta: {
    title: string;
  };
}

const storesTagsViewRoutes = useTagsViewRoutesStore();
const { tagsViewRoutes } = storeToRefs(storesTagsViewRoutes);
const layoutMenuAutocompleteRef = ref<any>(null);
const { t } = useI18n();
const router = useRouter();

const state = reactive<SearchState>({
  isShowSearch: false,
  menuQuery: '',
  tagsViewList: [],
});

const { isShowSearch, menuQuery } = toRefs(state);

// 初始化菜单数据
const initTagsView = () => {
  if (state.tagsViewList.length > 0) return false;
  tagsViewRoutes.value.forEach((v: any) => {
    if (!v.meta?.isHide) state.tagsViewList.push({ ...v });
  });
};

// 搜索弹窗打开
const openSearch = () => {
  state.menuQuery = '';
  state.isShowSearch = true;
  initTagsView();
  nextTick(() => {
    setTimeout(() => {
      layoutMenuAutocompleteRef.value?.focus?.();
    });
  });
};

// 搜索弹窗关闭
const closeSearch = () => {
  state.isShowSearch = false;
};

// 菜单搜索过滤
const createFilter = (queryString: string) => {
  return (restaurant: Restaurant) => {
    return (
      restaurant.path.toLowerCase().includes(queryString.toLowerCase()) ||
      restaurant.meta.title.toLowerCase().includes(queryString.toLowerCase()) ||
      t(restaurant.meta.title).toLowerCase().includes(queryString.toLowerCase())
    );
  };
};

// 菜单搜索数据过滤
const menuSearch = (queryString: string, cb: Function) => {
  let results = queryString
    ? state.tagsViewList.filter(createFilter(queryString) as any)
    : state.tagsViewList;
  cb(results);
};

// 当前菜单选中时
const onHandleSelect = (item: any) => {
  let { path, redirect, children } = item;
  if (item.meta?.isLink && !item.meta?.isIframe) window.open(item.meta.isLink);
  else if (redirect) router.push(redirect);
  else children ? router.push(children[0]) : router.push(path);
  closeSearch();
};

defineExpose({
  openSearch,
});
</script>

<style scoped lang="scss">
.layout-search-dialog {
  position: relative;
  :deep(.el-dialog) {
    .el-dialog__header,
    .el-dialog__body {
      display: none;
    }
    .el-dialog__footer {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      top: -53vh;
    }
  }
  :deep(.el-autocomplete) {
    width: 560px;
    position: absolute;
    top: 150px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
