<template>
  <div class="system-job-container">
    <el-dialog v-model="state.isShowDialog" top="20px" width="75%" center>
      <template #header>
        <div style="font-size: large"
             v-drag="['.system-job-container .el-dialog', '.system-job-container .el-dialog__header']">{{ title }}
        </div>
      </template>
      <el-card shadow="always">
        <el-form :model="state.queryParams" ref="queryForm" :inline="true" label-width="68px">
          <el-form-item label="任务名称" prop="periodic_task_name">
            <el-input
                placeholder="请输入任务名称模糊查询"
                clearable
                @keyup.enter="handleQuery"
                style="width: 240px"
                v-model="state.queryParams.periodic_task_name"
            />
          </el-form-item>
          <el-form-item label="执行方法" prop="task_name">
            <el-input
                placeholder="请输入任务执行方法"
                clearable
                @keyup.enter="handleQuery"
                style="width: 240px"
                v-model="state.queryParams.task_name"
            />
          </el-form-item>
          <el-form-item label="任务ID" prop="task_id">
            <el-input
                placeholder="请输入任务ID"
                clearable
                @keyup.enter="handleQuery"
                style="width: 240px"
                v-model="state.queryParams.task_id"
            />
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
        <el-table
            v-loading="state.loading"
            :data="state.tableData"
        >
          <el-table-column label="序号" width="55" prop="id"/>
          <el-table-column label="任务ID" width="160" align="center" prop="task_id"/>
          <el-table-column
              label="任务名称"
              align="center"
              prop="periodic_task_name"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="执行参数"
              align="center"
              prop="task_kwargs"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="执行方法"
              align="center"
              prop="task_name"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="执行状态"
              align="center"
              prop="status"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="执行结果"
              width="200"
              align="center"
              prop="result"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="创建时间"
              align="center"
              prop="date_created"
              :show-overflow-tooltip="true"
          />
          <el-table-column
              label="完成时间"
              align="center"
              prop="date_done"
              :show-overflow-tooltip="true"
          />
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
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {reactive} from "vue";
import {listTaskResult} from "@/api/tool/job";

const props = defineProps({
  title: {
    type: String,
    default: () => "",
  },
})

const state = reactive({
  // 是否显示弹出层
  isShowDialog: false,
  loading: false,
  // 定时任务表格数据
  tableData: [],
  // 总条数
  total: 0,
  // 查询参数
  queryParams: {
    // 页码
    page: 1,
    // 每页大小
    pageSize: 10,
    periodic_task_name: undefined,
    task_name: undefined,
    task_id: undefined,
  },
})
/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.periodic_task_name = undefined;
  state.queryParams.task_name = undefined;
  state.queryParams.task_id = undefined;
  handleQuery();
};

/** 查询定时任务日志列表 */
const handleQuery = () => {
  state.loading = true;
  listTaskResult(state.queryParams).then((response) => {
        state.tableData = response.data.data;
        state.total = response.data.total;
        state.loading = false;
      }
  );
};
// 打开弹窗
const openDialog = (row: any) => {
  state.queryParams.periodic_task_name = JSON.parse(JSON.stringify(row)).name;
  handleQuery();
  state.isShowDialog = true;
  state.loading = false;
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

defineExpose({
  openDialog,
});
</script>
