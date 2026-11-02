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
        <el-form-item label="参数名称" prop="configName">
          <el-input
              placeholder="参数名称模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.configName"
          />
        </el-form-item>
        <el-form-item label="参数键名" prop="configKey">
          <el-input
              placeholder="参数键名模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.configKey"
          />
        </el-form-item>
        <el-form-item label="系统内置" prop="configType">
          <el-select
              v-model="state.queryParams.configType"
              placeholder="系统内置"
              clearable
              style="width: 240px"
          >
            <el-option
                v-for="dict in state.typeOptions"
                :key="dict.dictValue"
                :label="dict.dictLabel"
                :value="dict.dictValue"
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
          <span class="card-header-text">配置列表</span>
          <div>
            <el-button
                type="primary"
                plain
                @click="onOpenAddModule"
                v-auth="'system:config:add'"
            >
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
            <el-button
                type="danger"
                plain
                :disabled="state.multiple"
                v-auth="'system:config:delete'"
                @click="onTabelRowDel"
            >
              <SvgIcon name="elementDelete"/>
              删除
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
        <el-table-column label="参数主键" align="center" prop="configId"/>
        <el-table-column
            label="参数名称"
            align="center"
            prop="configName"
            :show-overflow-tooltip="true"
        />
        <el-table-column
            label="参数键名"
            align="center"
            prop="configKey"
            :show-overflow-tooltip="true"
        />
        <el-table-column label="参数键值" align="center" prop="configValue"/>
        <el-table-column
            label="系统内置"
            align="center"
            prop="configType"
        >
          <template #default="scope">
            <el-tag
                :type="scope.row.configType === '1' ? 'danger' : 'success'"
                disable-transitions
            >{{ typeFormat(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
            label="备注"
            align="center"
            prop="remark"
            :show-overflow-tooltip="true"
        />
        <el-table-column
            label="创建时间"
            align="center"
            prop="createTime"
            width="180"
        >
          <template #default="scope">
            <span>{{ dateStrFormat(scope.row.createTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column
            label="操作"
            align="center"
            width="200"
            class-name="medium-padding fixed-width"
        >
          <template #default="scope">
            <el-popover  placement="left">
              <template #reference>
                <el-button type="primary" circle ><SvgIcon name="elementStar"/></el-button>
              </template>
              <div>
                <el-button text type="primary" v-auth="'system:config:edit'" @click="onOpenEditModule(scope.row)">
                  <SvgIcon name="elementEdit"/>
                  修改
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'system:config:delete'" @click="onTabelRowDel(scope.row)">
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
    <!-- 添加或修改配置参数对话框 -->
    <EditModule ref="editModuleRef" :title="state.title"/>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, getCurrentInstance, onUnmounted } from "vue";
import { listConfig, delConfig, exportConfig } from "@/api/system/config";
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
  listApi: listConfig,
  deleteApi: delConfig,
  exportApi: exportConfig,
  title: "参数",
  defaultParams: {
    configName: undefined,
    configKey: undefined,
    configType: undefined,
  },
});

const state = reactive({
  title: "",
  loading,
  tableData,
  total,
  queryParams,
  multiple,
  typeOptions: [],
});

// 配置参数状态配置参数翻译
const typeFormat = (row: any) => {
  return proxy.selectDictLabel(state.typeOptions, row.configType);
};

// 打开新增配置参数弹窗
const onOpenAddModule = () => {
  state.title = "添加配置参数";
  editModuleRef.value.openDialog({});
};

// 打开编辑配置参数弹窗
const onOpenEditModule = (row: object) => {
  state.title = "修改配置参数";
  editModuleRef.value.openDialog(row);
};

const onTabelRowDel = handleDelete;

// 页面加载时
onMounted(() => {
  handleQuery();
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.typeOptions = response.data;
  });
  proxy.mittBus.on("onEditConfigModule", () => {
    handleQuery();
  });
});

// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditConfigModule");
});
</script>
