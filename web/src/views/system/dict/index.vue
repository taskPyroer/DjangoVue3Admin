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
        <el-form-item label="关键词" prop="search">
          <el-input
              placeholder="请输入字典名称 类型模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.search"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select
              v-model="state.queryParams.status"
              placeholder="字典状态"
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
          <span class="card-header-text">字典列表</span>
          <div>
            <el-button
                type="primary"
                plain
                v-auth="'system:dictT:add'"
                @click="onOpenAddModule"
            >
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
            <el-button
                type="danger"
                plain
                v-auth="'system:dictT:delete'"
                :disabled="state.multiple"
                @click="onTabelRowDel"
            >
              <SvgIcon name="elementDelete"/>
              删除
            </el-button>
          </div>
        </div>
      </template>
      <!--数据表格-->
      <el-table v-loading="state.loading" border :data="state.tableData" @selection-change="handleSelectionChange">
        <el-table-column type="selection" align="center"/>
        <el-table-column label="字典编号" align="center" prop="id"/>
        <el-table-column label="字典名称" align="center" prop="dict_name" :show-overflow-tooltip="true"/>
        <el-table-column label="字典类型" align="center" prop="dict_type" :show-overflow-tooltip="true"/>
        <el-table-column label="备注" align="center" prop="remark" :show-overflow-tooltip="true"/>
        <el-table-column label="状态" align="center" prop="status">
          <template #default="scope">
            <el-tag
                :type="scope.row.status === '1' ? 'danger' : 'success'"
                disable-transitions
            >{{ statusFormat(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
            label="操作"
            align="center"
            width="350"
            class-name="medium-padding fixed-width"
        >
          <template #default="scope">
            <el-popover placement="left">
              <template #reference>
                <el-button type="primary" circle>
                  <SvgIcon name="elementStar"/>
                </el-button>
              </template>
              <div>
                <el-button text type="primary" @click="editDictItem(scope.row)">
                  <SvgIcon name="elementTools"/>
                  字典配置
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'system:dictT:edit'" @click="onOpenEditModule(scope.row)">
                  <SvgIcon name="elementEdit"/>
                  修改
                </el-button>
              </div>
              <div>
                <el-button v-if="scope.row.parentId != 0" text type="primary" v-auth="'system:dictT:delete'"
                           @click="onTabelRowDel(scope.row)">
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
    <!-- 添加或修改字典对话框 -->
    <EditModule ref="editModuleRef" :title="state.title"/>

    <!-- 字典列表对话框 -->
    <DictList ref="dictItemModuleRef"/>
  </div>
</template>
<!--使用 setup 语法糖-->
<script lang="ts" setup>
import {
  // toRefs,
  ref,
  reactive,
  onMounted,
  getCurrentInstance,
  onUnmounted,
} from "vue";
import {ElMessageBox, ElMessage} from "element-plus";
import {listType, delType} from "@/api/system/dict/type";
import EditModule from "./component/editModule.vue";
import DictList from "./component/dictList.vue";


const {proxy} = getCurrentInstance() as any;
const editModuleRef = ref();
const dictItemModuleRef = ref();
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
  // 字典表格数据
  tableData: [],
  // 总条数
  total: 0,
  // 状态数据字典
  statusOptions: [{
    dict_value: "0",
    dict_label: "正常"
  }, {
    dict_value: "1",
    dict_label: "禁用"
  }],
  // 查询参数
  queryParams: {
    // 页码
    page: 1,
    // 每页大小
    pageSize: 10,
    search: undefined,
    status: undefined,
  },
  //字典数据表单参数
  dictItemForm: [],
});
// const {loading, multiple, title, tableData, total, statusOptions, queryParams} = toRefs(state)
/** 查询字典列表 */
const handleQuery = () => {
  state.loading = true;
  listType(state.queryParams).then(
      (response) => {
        state.tableData = response.data.data;
        state.total = response.data.total;
        state.loading = false;
      }
  );
};
/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.search = undefined;
  state.queryParams.status = undefined;
  handleQuery();
};

const statusFormat = (row: any) => {
  return proxy.selectDictLabel(state.statusOptions, row.status);
};

// 打开新增字典弹窗
const onOpenAddModule = () => {
  state.title = "添加字典";
  editModuleRef.value.openDialog({});
};
// 打开编辑字典弹窗
const onOpenEditModule = (row: object) => {
  state.title = "修改字典";
  editModuleRef.value.openDialog(row);
};
/** 删除按钮操作 */
const onTabelRowDel = (row: any) => {
  const dictIds = row.id || state.ids;
  ElMessageBox({
    message: '是否确认删除字典编号为"' + dictIds + '"的数据项?',
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(function () {
    return delType(dictIds).then(() => {
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

//分页页面大小发生变化
const handleSizeChange = (val: any) => {
  state.queryParams.pageSize = val;
  handleQuery();
};
//当前页码发生变化
const handleCurrentChange = (val: any) => {
  state.queryParams.page = val;
  handleQuery();
};
//编辑字典数据
const editDictItem = (record: any) => {
  dictItemModuleRef.value.openDrawer(record);
};

// 页面加载时
onMounted(() => {
  // 查询字典信息
  handleQuery();
  proxy.mittBus.on("onEditPostModule", () => {
    handleQuery();
  });
});
// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditPostModule");
});

</script>
