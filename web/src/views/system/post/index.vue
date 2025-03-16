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
import {
  ref,
  reactive,
  onMounted,
  getCurrentInstance,
  onUnmounted,
} from "vue";
import {ElMessageBox, ElMessage} from "element-plus";
import {listPost, delPost, exportPost} from "@/api/system/post";
import EditModule from "./component/editModule.vue";
import {handleFileError} from "@/utils/export";
const {proxy} = getCurrentInstance() as any;
const editModuleRef = ref();
const state = reactive({
  // 遮罩层
  loading: true,
  // 选中数组
  ids: [],
  // 非单个禁用
  single: true,
  // 非多个禁用
  multiple: true,
  // 弹出层标题
  title: "",
  // 岗位表格数据
  tableData: [],
  // 总条数
  total: 0,
  // 状态数据字典
  statusOptions: [],
  // 查询参数
  queryParams: {
    // 页码
    page: 1,
    // 每页大小
    pageSize: 10,
    search: '',
    status: undefined,
  },
});

/** 查询岗位列表 */
const handleQuery = () => {
  state.loading = true;
  listPost(state.queryParams).then((response) => {
    state.tableData = response.data.data;
    state.total = response.data.total;
    state.loading = false;
  });
};
/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.search = '';
  state.queryParams.status = undefined;
  handleQuery();
};

const handleCurrentChange = (val: number) => {
  state.queryParams.page = val
  handleQuery()
}
const handleSizeChange = (val: number) => {
  state.queryParams.pageSize = val
  handleQuery()
}

const statusFormat = (row: any) => {
  return proxy.selectDictLabel(state.statusOptions, row.status);
};

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
/** 删除按钮操作 */
const onTabelRowDel = (row: any) => {
  const postIds = row.id || state.ids;
  ElMessageBox({
    message: '是否确认删除岗位编号为"' + postIds + '"的数据项?',
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(function () {
    return delPost(postIds).then(() => {
      handleQuery();
      ElMessage.success("删除成功");
    });
  });
};
// 多选框选中数据
const handleSelectionChange = (selection: any) => {
  state.ids = selection.map((item: any) => item.id);
  state.single = selection.length != 1;
  state.multiple = !selection.length;
};

/** 导出按钮操作 */
const handleExport = () => {

  ElMessageBox({
    message: "是否确认导出所有数据项?",
    title: "警告",
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
      .then(function () {
        return exportPost();
      })
      .then((response: any) => {
        let data: any = new Date().getTime() / 1000
        let time = parseInt(data) + '';
        handleFileError(response, "岗位表_" + time + ".xls")
      });
};

// 页面加载时
onMounted(() => {
  // 查询岗位信息
  handleQuery();
  // 查询岗位状态数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
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
