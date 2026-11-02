<template>
  <div class="system-user-container app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form
          :model="state.queryParams"
          ref="queryForm"
          :inline="true"
      >
        <el-form-item label="关键词" prop="search">
          <el-input
              size="default"
              placeholder="请输入关键词模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 180px"
              v-model="state.queryParams.search"
          />
        </el-form-item>
        <el-form-item label="请求地址" prop="request_modular">
          <el-input
              placeholder="请输入操作模块模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 180px"
              v-model="state.queryParams.request_modular"
          />
        </el-form-item>
        <el-form-item label="操作模块" prop="request_path">
          <el-input
              placeholder="请输入请求地址模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 180px"
              v-model="state.queryParams.request_path"
          />
        </el-form-item>
        <el-form-item label="请求方法" prop="businessType" v-if="state.showOtherSearch">
          <el-select
              v-model="state.queryParams.request_method"
              placeholder="请求方法"
              clearable
              style="width: 180px"
          >
            <el-option
                v-for="dict in state.methodOptions"
                :key="dict.dict_value"
                :label="dict.dict_label"
                :value="dict.dict_value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="IP地址" prop="request_ip" v-if="state.showOtherSearch">
          <el-input
              placeholder="请输入IP地址模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 180px"
              v-model="state.queryParams.request_ip"
          />
        </el-form-item>
        <el-form-item label="操作时间" prop="expire_time" v-if="state.showOtherSearch">
          <el-date-picker
              v-model="state.expire_time"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              @change="handleDateChange">
          </el-date-picker>
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
          <el-button @click="clickMore" v-if="!state.showOtherSearch">
            <SvgIcon name="elementArrowDown"/>
            展开
          </el-button>
          <el-button @click="clickMore" v-if="state.showOtherSearch">
            <SvgIcon name="elementArrowUp"/>
            收起
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span class="card-header-text">操作日志</span>
          <div>
            <el-button
                type="danger"
                plain
                :disabled="state.multiple"
                @click="onTabelRowDel"
                v-auth="'log:operation:delete'"
            >
              <SvgIcon name="elementDelete"/>
              删除
            </el-button>
            <el-button
                type="danger"
                plain
                @click="handleClean"
                v-auth="'log:operation:clean'"
            >
              <SvgIcon name="elementDelete"/>
              清空
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
        <el-table-column label="日志编号" align="center" width="120" prop="id"/>
        <el-table-column label="操作模块" align="center" prop="request_modular"/>
        <el-table-column label="请求地址" align="center" prop="request_path"/>
        <el-table-column label="请求方法" align="center" prop="request_method"/>
        <el-table-column label="操作人员" align="center" prop="creator_name"/>
        <el-table-column label="请求浏览器" align="center" prop="request_browser" :show-overflow-tooltip="true"/>
        <el-table-column label="响应码" align="center" prop="response_code">
          <template #default="scope">
            <el-tag :type="scope.row.response_code === '200' ? 'success' : 'default'">
              {{ scope.row.response_code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作日期" align="center" prop="create_datetime"/>
        <el-table-column label="返回信息" align="center" prop="json_result" :show-overflow-tooltip="true"/>
        <el-table-column
            label="操作"
            align="center"
            class-name="small-padding fixed-width"
            fixed="right"
        >
          <template #default="scope">
            <el-button text type="primary" @click="handleView(scope.row)">
              <SvgIcon name="elementView"/>
              详细
            </el-button>
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
            :page-sizes="[10, 20, 30, 40]"
            :page-size="state.queryParams.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    <!-- 操作日志详细 -->
    <el-dialog title="操作日志详细" v-model="state.open" width="700px" center append-to-body>
      <el-form ref="ruleFormRef" :model="state.modelForm" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="操作模块：">{{ state.modelForm.request_modular }}</el-form-item>
            <el-form-item label="登录信息：">{{ state.modelForm.creator_name }} / {{ state.modelForm.request_ip }} /
              {{ state.modelForm.request_browser }}
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="请求地址：">{{state.modelForm.request_path }}</el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="操作方法：">{{state.modelForm.request_method}}</el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="请求参数：">{{state.modelForm.request_body }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="操作状态：">{{ state.modelForm.response_code }}</el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="操作时间：">{{state.modelForm.create_datetime }}</el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="返回信息：">{{state.modelForm.json_result }}</el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="state.open = false">关 闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="Operlog">
import { reactive, onMounted, getCurrentInstance } from "vue";
import {
  listOperInfo,
  delOperInfo,
  cleanOpernfo,
} from "@/api/log/oper";
import { ElMessageBox, ElMessage } from "element-plus";
import { dateStrFormat } from "@/utils/formatTime";
import SvgIcon from "@/components/svgIcon/index.vue";
import { useCrud } from "@/hooks/useCrud";

const { proxy } = getCurrentInstance() as any;

const {
  loading,
  tableData,
  total,
  queryParams,
  multiple,
  handleQuery,
  resetQuery: crudResetQuery,
  handleCurrentChange,
  handleSizeChange,
  handleSelectionChange,
  handleDelete,
} = useCrud({
  listApi: listOperInfo,
  deleteApi: delOperInfo,
  title: "操作日志",
  defaultParams: {
    start_time: undefined,
    end_time: undefined,
    search: undefined,
    request_modular: undefined,
    request_path: undefined,
    businessType: undefined,
    request_ip: undefined,
    request_method: undefined,
  },
});

const state = reactive({
  loading,
  total,
  tableData,
  multiple,
  title: "",
  open: false,
  showOtherSearch: false,
  modelForm: {} as any,
  methodOptions: {},
  expire_time: [],
  queryParams,
});

/** 重置按钮操作 */
const resetQuery = () => {
  state.expire_time = [];
  crudResetQuery(() => {
    state.queryParams.start_time = undefined;
    state.queryParams.end_time = undefined;
    state.queryParams.search = undefined;
    state.queryParams.request_modular = undefined;
    state.queryParams.request_path = undefined;
    state.queryParams.request_ip = undefined;
    state.queryParams.request_method = undefined;
    state.queryParams.page = 1;
    state.queryParams.pageSize = 10;
  });
};

/** 清空按钮操作 */
const handleClean = () => {
  ElMessageBox({
    message: "是否确认清空所有操作日志数据项?",
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => cleanOpernfo())
    .then(() => {
      handleQuery();
      ElMessage.success("清空成功");
    });
};

const onTabelRowDel = handleDelete;

/** 详细按钮操作 */
const handleView = (row: any) => {
  state.open = true;
  state.modelForm = row;
};

/** 点击查看更多或收起 */
const clickMore = () => {
  state.showOtherSearch = !state.showOtherSearch;
  window.dispatchEvent(new Event("resize"));
};

/** 时间范围处理 */
const handleDateChange = () => {
  const expire_time = state.expire_time;
  if (expire_time && expire_time.length === 2) {
    state.queryParams.start_time = dateStrFormat(expire_time[0]);
    state.queryParams.end_time = dateStrFormat(expire_time[1]);
  } else {
    state.queryParams.start_time = undefined;
    state.queryParams.end_time = undefined;
  }
};

/** 页面加载时调用 */
onMounted(() => {
  handleQuery();
  proxy.getDicts("sys_method_api").then((response: any) => {
    state.methodOptions = response?.data?.data || [];
  });
});
</script>

<style>
</style>
