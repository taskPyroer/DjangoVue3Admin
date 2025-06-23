<template>
  <div class="app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form :model="state.queryParams" ref="queryForm" :inline="true" label-width="68px">
        <el-form-item label="标题" prop="title">
          <el-input
              placeholder="请输入标题模糊查询"
              clearable
              @keyup.enter.native="handleQuery"
              v-model="state.queryParams.search"
          />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-input
              placeholder="请输入分类"
              clearable
              v-model="state.queryParams.category"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
              v-model="state.queryParams.status"
              placeholder="状态"
              clearable
              style="width: 180px;"
          >
            <el-option
                v-for="dict in state.statusOptions"
                :key="dict.dict_value"
                :label="dict.dict_label"
                :value="dict.dict_value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" plain @click="handleQuery">
            <SvgIcon name="elementSearch"/>
            搜索
          </el-button>
          <el-button @click="resetQuery">
            <SvgIcon name="elementRefresh"/>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="card-header-text">示例列表</span>
          <div>
            <el-button type="primary"
                       plain
                       v-auth="'system:example:add'"
                       @click="onOpenAddModule">
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
          </div>
        </div>
      </template>
      <!--数据表格-->
      <el-table
          v-loading="state.loading"
          :data="state.tableData"
          border
      >
        <el-table-column
            prop="title"
            label="标题"
            width="200"
        ></el-table-column>
        <el-table-column
            prop="content"
            label="内容"
            show-overflow-tooltip
        ></el-table-column>
        <el-table-column
            prop="category"
            label="分类"
            width="120"
        ></el-table-column>
        <el-table-column
            prop="status"
            label="状态"
            width="100"
        >
          <template #default="scope">
            <el-tag
                :type="scope.row.status === '1' ? 'danger' : 'success'"
                disable-transitions
            >{{ statusFormat(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
            prop="create_datetime"
            label="创建时间"
            width="180"
        >
          <template #default="scope">
            <span>{{ dateStrFormat(scope.row.create_datetime) }}</span>
          </template>
        </el-table-column>
        <el-table-column
            label="操作"
            align="center"
            class-name="small-padding fixed-width"
            fixed="right"
            width="180"
        >
          <template #default="scope">
            <el-button text type="primary" v-auth="'system:example:edit'" @click="onOpenEditModule(scope.row)">
              <SvgIcon name="elementEdit"/>
              修改
            </el-button>
            <el-button text type="primary" v-auth="'system:example:delete'"
                       @click="onTabelRowDel(scope.row)">
              <SvgIcon name="elementDelete"/>
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页-->
      <div v-show="state.total > 0">
        <el-divider></el-divider>
        <el-pagination
            background
            :total="state.total"
            :page-sizes="[10, 20, 30]"
            v-model:current-page="state.queryParams.page"
            v-model:page-size="state.queryParams.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </el-card>
    <!-- 添加或修改示例对话框 -->
    <EditModule ref="editModuleRef" :title="state.title"/>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, onMounted, getCurrentInstance, onUnmounted, watch} from "vue";
import {ElMessageBox, ElMessage} from "element-plus";
import {listExample, delExample} from "@/api/system/example";
import EditModule from "./component/editModule.vue";
import {dateStrFormat} from "@/utils/formatTime";
// 移除不存在的Pagination组件导入

const {proxy} = getCurrentInstance() as any;
const editModuleRef = ref();
const state = reactive({
  // 遮罩层
  loading: true,
  // 弹出层标题
  title: "",
  // 总条数
  total: 0,
  // 示例表格数据
  tableData: [] as any,
  // 状态数据字典
  statusOptions: [],
  // 查询参数
  queryParams: {
    search: undefined,
    category: undefined,
    status: undefined,
    pageSize: 10,
    page: 1
  },
});

/** 查询示例列表 */
const handleQuery = () => {
  state.loading = true;
  listExample(state.queryParams).then((response: any) => {
    state.tableData = response.data.data;
    state.total = response.data.count;
    state.loading = false;
  });
};
/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.search = undefined;
  state.queryParams.category = undefined;
  state.queryParams.status = undefined;
  handleQuery();
};

// 状态字典翻译
const statusFormat = (row: any) => {
  return proxy.selectDictLabel(state.statusOptions, row.status);
};

// 打开新增示例弹窗
const onOpenAddModule = () => {
  state.title = "添加示例";
  editModuleRef.value.openDialog({});
};
// 打开编辑示例弹窗
const onOpenEditModule = (row: object) => {
  state.title = "修改示例";
  editModuleRef.value.openDialog(row);
};
/** 删除按钮操作 */
const onTabelRowDel = (row: any) => {
  ElMessageBox({
    message: '是否确认删除标题为"' + row.title + '"的数据项?',
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(function () {
    return delExample(row.id).then(() => {
      handleQuery();
      ElMessage.success("删除成功");
    });
  });
};

// 监听分页参数变化
watch(
  () => [state.queryParams.page, state.queryParams.pageSize],
  () => {
    handleQuery();
  }
);
// 页面加载时
onMounted(() => {
  // 查询示例信息
  handleQuery();
  // 查询状态数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
  });
  proxy.mittBus.on("onEditExampleModule", (res: any) => {
    handleQuery();
  });
});
// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditExampleModule");
});
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-text {
  font-size: 16px;
  font-weight: bold;
}
</style>