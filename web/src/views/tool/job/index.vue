<template>
  <div class="app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form :model="state.queryParams" ref="queryForm" :inline="true" label-width="68px">
        <el-form-item label="任务名称" prop="jobName">
          <el-input
              placeholder="请输入任务名称模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 240px"
              v-model="state.queryParams.name"
          />
        </el-form-item>
        <el-form-item label="任务状态" prop="enabled">
          <el-select
              v-model="state.queryParams.enabled"
              placeholder="请选择任务状态"
              clearable
              style="width: 240px"
          >
            <el-option
                v-for="dict in state.enabledOptions"
                :key="dict.dictValue"
                :label="dict.dictLabel"
                :value="dict.dictValue"
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
          <span class="card-header-text">定时任务列表</span>
          <div>
            <el-button
                type="primary"
                plain
                @click="onOpenAddModule"
                v-auth="'tool:job:add'"
            >
              <SvgIcon name="elementPlus"/>
              新增
            </el-button>
            <el-button
                type="danger"
                plain
                :disabled="state.multiple"
                @click="onTabelRowDel"
                v-auth="'tool:job:delete'"
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
        <el-table-column label="任务编号" align="center" prop="id"/>
        <el-table-column
            label="任务名称"
            align="center"
            prop="name"
            width="160"
            :show-overflow-tooltip="true"
        />
        <el-table-column
            label="任务类型"
            align="center"
            prop="type"
        >
          <template #default="scope">
            {{ scope.row.type == 0 ? "间隔任务" : "周期任务" }}
          </template>
        </el-table-column>
        <el-table-column
            label="已运行次数"
            align="center"
            prop="total_run_count"
            width="120"
            :show-overflow-tooltip="true"
        />
        <el-table-column
            label="任务参数"
            align="center"
            prop="kwargs"
            width="120"
            :show-overflow-tooltip="true"
        />
        <el-table-column
            label="一次性任务"
            align="center"
            prop="total_run_count"
            width="120"
            :show-overflow-tooltip="true">
          <template #default="scope">
            <el-tag v-if="scope.row.one_off" type="success">是</el-tag>
            <el-tag v-else type="info">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column
            label="执行状态"
            align="center"
            width="120"
            :show-overflow-tooltip="true">
          <template #default="scope">
            <el-tag v-if="scope.row.enabled">正常</el-tag>
            <el-tag v-else type="danger">停止</el-tag>
          </template>
        </el-table-column>
        <el-table-column
            label="执行方法"
            align="center"
            prop="task"
            width="200"
            :show-overflow-tooltip="true"
        />
        <el-table-column label="执行时间" align="center" width="120" :show-overflow-tooltip="true">
          <template #default="scope">
            <span v-if="scope.row.type">{{ scope.row.crontab }}</span>
            <span v-else>{{
                "间隔" + scope.row.interval.every + state.intervalList.filter(item => scope.row.interval.period === item.id)[0].name
              }}</span>
          </template>
        </el-table-column>
        <el-table-column
            label="备注"
            align="center"
            prop="description"
            width="160"
            :show-overflow-tooltip="true"
        />
        <el-table-column label="更新时间" align="center" prop="date_changed" width="180">
          <template #default="scope">
            <span>{{ dateStrFormat(scope.row.date_changed) }}</span>
          </template>
        </el-table-column>
        <el-table-column
            label="操作"
            align="center"
            width="120"
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
                <el-button text type="primary" v-auth="'tool:job:run'" @click="handleRun(scope.row)">
                  <SvgIcon name="elementSwitchButton"/>
                  {{ scope.row.enabled == true ? "停止" : "启动" }}
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'tool:job:edit'" @click="onOpenEditModule(scope.row)">
                  <SvgIcon name="elementEdit"/>
                  编辑
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'tool:job:log'" @click="onOpenCronLogs(scope.row)">
                  <SvgIcon name="elementTickets"/>
                  日志
                </el-button>
              </div>
              <div>
                <el-button text type="primary" v-auth="'tool:job:delete'" @click="onTabelRowDel(scope.row)">
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
    <CronLogs ref="cronLogsRef" :title="state.title"/>
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
import {
  listJob,
  runStopJob,
  delJob,
} from "@/api/tool/job";
import EditModule from "./component/editModule.vue";
import CronLogs from "./component/cronLogs.vue";
import {useRouter} from "vue-router";
import {dateStrFormat} from "@/utils/formatTime";

const {proxy} = getCurrentInstance() as any;
const editModuleRef = ref();
const cronLogsRef = ref();
const ruleFormRef = ref<HTMLElement | null>(null);
const router = useRouter();
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
  // 定时任务表格数据
  tableData: [],
  // 总条数
  total: 0,
  // 是否显示弹出层
  open: false,
  // 表单参数
  modelForm: {},
  // 状态字典
  enabledOptions: [
    {dictValue: false, dictLabel: '停止'},
    {dictValue: true, dictLabel: '开启'},
  ],
  // 查询参数
  queryParams: {
    // 页码
    page: 1,
    // 每页大小
    pageSize: 10,
    name: undefined,
    enabled: undefined,
  },
  // 间隔类型
  intervalList: [
    {id: 'days', name: '天'},
    {id: 'hours', name: '小时'},
    {id: 'minutes', name: '分钟'},
    {id: 'seconds', name: '秒'},
    {id: 'microseconds', name: '微秒'},
  ]
});

/** 查询定时任务列表 */
const handleQuery = () => {
  state.loading = true;
  listJob(state.queryParams).then((response) => {
        state.tableData = response.data.data;
        state.total = response.data.total;
        state.loading = false;
      }
  );
};
/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.name = undefined;
  state.queryParams.enabled = undefined;
  handleQuery();
};

// 打开新增定时任务弹窗
const onOpenAddModule = () => {
  state.title = "添加定时任务";
  editModuleRef.value.openDialog({});
};
// 打开编辑定时任务弹窗
const onOpenEditModule = (row: object) => {
  state.title = "修改定时任务";
  editModuleRef.value.openDialog(row);
};
// 打开日志弹窗
const onOpenCronLogs = (row: object) => {
  state.title = "任务日志";
  cronLogsRef.value.openDialog(row);
}
/** 删除按钮操作 */
const onTabelRowDel = (row: any) => {
  const jobIds = row.id || state.ids;
  ElMessageBox({
    message: '是否确认删除定时任务编号为"' + jobIds + '"的数据项?',
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(function () {
    return delJob(jobIds).then(() => {
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

const handleRun = (row: any) => {
  let text = row.enabled == true ? "停止" : "启动"
  ElMessageBox({
    message: '确认要立即' + text + '"' + row.name + '"任务吗?',
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
      .then(function () {
        if (row.enabled == false) {
          row.enabled = true
        } else {
          row.enabled = false
        }
        runStopJob(row.id, row.enabled).then((res: any) => {
          handleQuery();
        })
      })
      .then(() => {
        ElMessage({
          message: text + "执行成功",
          type: 'success',
        });
      });
};
// 页面加载时
onMounted(() => {
  // 查询定时任务信息
  handleQuery();
  proxy.mittBus.on("onEditJobModule", (res: any) => {
    handleQuery();
  });
});
// 页面卸载时
onUnmounted(() => {
  proxy.mittBus.off("onEditJobModule");
});
</script>
