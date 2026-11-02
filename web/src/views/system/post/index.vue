<template>
  <div class="app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form
          :model="state.queryParams"
          ref="queryForm"
          :inline="true"
          label-width="68px"
      >
        <el-form-item label="关键词" prop="postCode">
          <el-input
              placeholder="请输入岗位编码/岗位名称模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.search"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
              v-model="state.queryParams.status"
              placeholder="岗位状态"
              clearable
              style="width: 240px"
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
          <span class="card-header-text">岗位列表</span>
          <div>
            <el-button
                type="primary"
                plain
                v-auth="'system:post:add'"
                @click="onOpenAddModule"
            >
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
            <el-button
                type="danger"
                plain
                v-auth="'system:post:delete'"
                :disabled="state.multiple"
                @click="onTabelRowDel"
            >
              <SvgIcon name="elementDelete"/>
              删除
            </el-button>
            <el-button
                type="warning"
                plain
                v-auth="'system:post:export'"
                @click="handleExport"
            >
              <SvgIcon name="elementDownload"/>
              导出
            </el-button>
          </div>
        </div>
      </template>
      <!--数据表格-->
      <el-table
          v-loading="state.loading"
          :data="state.tableData"
          @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center"/>
        <el-table-column label="岗位编号" align="center" prop="id"/>
        <el-table-column label="岗位编码" align="center" prop="post_code"/>
        <el-table-column label="岗位名称" align="center" prop="post_name"/>
        <el-table-column label="岗位排序" align="center" prop="sort"/>
        <el-table-column label="备注" align="center" prop="remark"/>
        <el-table-column
            label="状态"
            align="center"
            prop="status"
        >
          <template #default="scope">
            <el-tag
                :type="scope.row.status === '0' ? 'success' : 'danger'"
                disable-transitions
            >{{ statusFormat(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
            label="操作"
            align="center"
            class-name="small-padding fixed-width"
            fixed="right"
        >
          <template #default="scope">
            <el-popover placement="left">
              <template #reference>
                <el-button type="primary" circle>
                  <SvgIcon name="elementStar"/>
                </el-button>
              </template>
              <div>
                <el-button text type="primary" v-auth="'system:post:edit'" @click="onOpenEditModule(scope.row)">
                  <SvgIcon name="elementEdit"/>
                  修改
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'system:post:delete'" @click="onTabelRowDel(scope.row)">
                  <SvgIcon name="elementDelete"/>
                  删除
                </el-button>
              </div>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页设置-->
      <div v-show="state.total > 0">
        <el-divider></el-divider>
        <el-pagination
            background
            :total="state.total"
            :current-page="state.queryParams.page"
            :page-size="state.queryParams.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    <!-- 添加或修改岗位对话框 -->
    <EditModule ref="editModuleRef" :title="state.title"/>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, getCurrentInstance, onUnmounted } from "vue";
import { listPost, delPost, exportPost } from "@/api/system/post";
import EditModule from "./component/editModule.vue";
import { useCrud } from "@/hooks/useCrud";

const { proxy } = getCurrentInstance() as any;
const editModuleRef = ref();

const {
  loading,
  tableData,
  total,
  queryParams,
  multiple,
  handleQuery,
  resetQuery,
  handleCurrentChange,
  handleSizeChange,
  handleSelectionChange,
  handleDelete,
  handleExport,
} = useCrud({
  listApi: listPost,
  deleteApi: delPost,
  exportApi: exportPost,
  exportPrefix: "岗位表",
  title: "岗位",
  defaultParams: {
    search: "",
    status: undefined,
  },
});

const state = reactive({
  title: "",
  statusOptions: [],
  loading,
  tableData,
  total,
  queryParams,
  multiple,
});

const statusFormat = (row: any) => {
  return proxy.selectDictLabel(state.statusOptions, row.status);
};

// 别名兼容模板事件绑定
const onTabelRowDel = handleDelete;

// 打开新增岗位弹窗
const onOpenAddModule = () => {
  state.title = "添加岗位";
  editModuleRef.value.openDialog({});
};

// 打开编辑岗位弹窗
const onOpenEditModule = (row: object) => {
  state.title = "修改岗位";
  editModuleRef.value.openDialog(row);
};

// 页面加载时
onMounted(() => {
  handleQuery();
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response?.data?.data || [];
  });
  proxy.mittBus.on("onEditPostModule", () => {
    handleQuery();
  });
});

// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditPostModule");
});
</script>
