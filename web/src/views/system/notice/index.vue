<template>
  <div class="app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form :model="state.queryParams" ref="queryForm" :inline="true" label-width="68px">
        <el-form-item label="信息类型" prop="tabActive">
          <el-select
              v-model="state.tabActive"
              placeholder="请选择信息类型"
              style="width: 140px"
          >
            <el-option
                v-for="item in state.tabOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="信息标题" prop="search">
          <el-input
              placeholder="请输入信息标题模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.search"
          />
        </el-form-item>
        <el-form-item label="通知类型" prop="target_type">
          <el-select
              v-model="state.queryParams.target_type"
              placeholder="请选择通知类型"
              clearable
              style="width: 240px"
          >
            <el-option
                v-for="dict in state.noticeTypeOptions"
                :key="dict.dict_value"
                :label="dict.dict_label"
                :value="dict.dict_value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button
              type="primary"
              plain
              @click="handleQuery"
          >
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
          <span class="card-header-text">信息列表</span>
          <div>
            <el-button type="primary" plain @click="onOpenAddModule" v-auth="'system:notice:add'">
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
            <el-button type="danger" plain :disabled="state.multiple" @click="onTabelRowDel" v-if="!state.tab"
                       v-auth="'system:notice:delete'">
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
        <el-table-column label="通知编号" align="center" prop="id"/>
        <el-table-column v-if="state.tab" label="是否已读" align="center" prop="is_read">
          <template #default="scope">
            <el-tag :type="scope.row.is_read ? 'success' : 'danger'">
              {{ scope.row.is_read ? '已读' : '未读' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="通知标题" align="center" prop="title" :show-overflow-tooltip="true"/>
        <el-table-column label="通知类型" align="center" prop="target_type" :formatter="noticeTypeFormat"/>
        <el-table-column label="通知内容" align="center" prop="content" :show-overflow-tooltip="true"/>
        <el-table-column label="通知时间" align="center" prop="create_datetime" width="180"/>
        <el-table-column label="备注" align="center" prop="remark"/>
        <el-table-column
            label="操作"
            align="center"
        >
          <template #default="scope">
            <el-popover placement="left">
              <template #reference>
                <el-button type="primary" circle>
                  <SvgIcon name="elementStar"/>
                </el-button>
              </template>
              <div>
                <el-button text type="primary" v-auth="'system:notice:view'" @click="handleRun(scope.row)">
                  <SvgIcon name="elementView"/>
                  查看
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'system:notice:delete'" @click="onTabelRowDel(scope.row)" v-if="!state.tab">
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
    <!-- 添加或修改定时任务对话框 -->
    <EditModule ref="editModuleRef" :title="state.title"/>
    <ViewModule ref="viewModuleRef"/>
  </div>
</template>

<script lang="ts" setup name="Notice">
import { ref, reactive, onMounted, getCurrentInstance, onUnmounted } from "vue";
import { listSendNotice, listReceiveNotice, delNotice } from "@/api/system/notice";
import EditModule from "./component/editModule.vue";
import ViewModule from "./component/viewModule.vue";
import { useCrud } from "@/hooks/useCrud";

const { proxy } = getCurrentInstance() as any;
const editModuleRef = ref();
const viewModuleRef = ref();
const ruleFormRef = ref<HTMLElement | null>(null);

const activeTab = ref<"receive" | "send">("receive");

const {
  loading,
  tableData,
  total,
  queryParams,
  multiple,
  handleQuery: crudQuery,
  resetQuery,
  handleCurrentChange,
  handleSizeChange,
  handleSelectionChange,
  handleDelete,
} = useCrud({
  listApi: (params) => (activeTab.value === "send" ? listSendNotice(params) : listReceiveNotice(params)),
  deleteApi: delNotice,
  title: "公告",
  defaultParams: {
    search: undefined,
    target_type: undefined,
  },
});

const state = reactive({
  title: "",
  loading,
  tableData,
  total,
  queryParams,
  multiple,
  noticeTypeOptions: [],
  tabActive: "receive",
  tabOptions: [
    { value: "send", label: "我的发布" },
    { value: "receive", label: "我的接收" },
  ],
  tab: true,
});

const handleQuery = () => {
  activeTab.value = state.tabActive as any;
  state.tab = state.tabActive === "receive";
  crudQuery();
};

const noticeTypeFormat = (row: any) => {
  return proxy.selectDictLabel(state.noticeTypeOptions, row.target_type);
};

// 打开新增公告弹窗
const onOpenAddModule = () => {
  state.title = "添加公告";
  editModuleRef.value.openDialog({});
};

const handleRun = (row: any) => {
  viewModuleRef.value.openDialog(row, state.noticeTypeOptions);
};

const onTabelRowDel = handleDelete;

// 页面加载时
onMounted(() => {
  handleQuery();
  proxy.getDicts("sys_notice_type").then((response: any) => {
    state.noticeTypeOptions = response?.data?.data || [];
  });
  proxy.mittBus.on("onEditNoticeModule", () => {
    handleQuery();
  });
});

// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditNoticeModule");
});
</script>

<style scoped lang="scss">
.el-descriptions {
  margin-top: 20px;
}

.cell-item {
  width: 100px;
  display: flex;
  align-items: center;
}
</style>
