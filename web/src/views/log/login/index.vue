
<template>
    <div class="system-user-container app-container">
        <el-card shadow="always">
        <!-- 查询 -->
        <el-form
                :model="state.queryParams"
                ref="queryForm"
                :inline="true"
                label-width="68px"
        >
            <el-form-item label="登录地点" prop="loginLocation">
                <el-input
                        placeholder="请输入登录地点模糊查询"
                        clearable
                        @keyup.enter="handleQuery"
                        style="width: 240px"
                        v-model="state.queryParams.loginLocation"
                />
            </el-form-item>
            <el-form-item label="用户名称" prop="userName">
                <el-input
                        placeholder="请输入用户名称模糊查询"
                        clearable
                        @keyup.enter="handleQuery"
                        style="width: 240px"
                        v-model="state.queryParams.username"
                />
            </el-form-item>
            <el-form-item>
                <el-button type="primary" plain @click="handleQuery"><SvgIcon name="elementSearch" />搜索</el-button>
                <el-button @click="resetQuery"><SvgIcon name="elementRefresh" />重置</el-button>
            </el-form-item>
        </el-form>
        </el-card>
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span class="card-header-text">登录日志</span>
            <div>
              <el-button
                  type="danger"
                  plain

                  :disabled="state.multiple"
                  @click="onTabelRowDel"
                  v-auth="'log:login:delete'"
              ><SvgIcon name="elementDelete" />删除</el-button>
              <el-button
                  type="danger"
                  plain

                  @click="handleClean"
                  v-auth="'log:login:clean'"
              ><SvgIcon name="elementDelete" />清空</el-button>
            </div>
          </div>
        </template>

        <!--数据表格-->
        <el-table
                v-loading="state.loading"
                :data="state.tableData"
                @selection-change="handleSelectionChange"
        >
            <el-table-column type="selection" width="55" align="center" />
            <el-table-column label="访问编号" align="center" prop="infoId" />
            <el-table-column label="用户名称" align="center" prop="username" />
            <el-table-column
                    label="登录地址"
                    align="center"
                    prop="ipaddr"
                    width="130"
                    :show-overflow-tooltip="true"
            />
            <el-table-column
                    label="登录地点"
                    align="center"
                    prop="loginLocation"
                    :show-overflow-tooltip="true"
            />
            <el-table-column label="浏览器" align="center" prop="browser" />
            <el-table-column label="操作系统" align="center" prop="os" />
            <el-table-column
                    label="登录状态"
                    align="center"
                    prop="status"
            >
                <template #default="scope">
                    <el-tag
                            :type="scope.row.status === '1' ? 'danger' : 'success'"
                            disable-transitions
                    >{{ statusFormat(scope.row)}}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作信息" align="center" prop="msg" />
            <el-table-column
                    label="登录日期"
                    align="center"
            >
                <template #default="scope">
                    <span>{{ dateStrFormat(scope.row.createTime) }}</span>
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
    </div>
</template>

<script lang="ts" setup name="Logininfo">
import { reactive, onMounted, getCurrentInstance } from "vue";
import { listLoginInfo, delLoginInfo, cleanLoginInfo } from "@/api/log/login";
import { ElMessageBox, ElMessage } from "element-plus";
import { useCrud } from "@/hooks/useCrud";

const { proxy } = getCurrentInstance() as any;

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
} = useCrud({
  listApi: listLoginInfo,
  deleteApi: delLoginInfo,
  title: "登录日志",
  defaultParams: {
    loginLocation: undefined,
    username: undefined,
  },
});

const state = reactive({
  loading,
  total,
  tableData,
  multiple,
  statusOptions: [],
  queryParams,
});

/** 清空按钮操作 */
const handleClean = () => {
  ElMessageBox({
    message: "是否确认清空所有登录日志数据项?",
    title: "警告",
    showCancelButton: true,
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => cleanLoginInfo())
    .then(() => {
      handleQuery();
      ElMessage.success("清空成功");
    });
};

const onTabelRowDel = handleDelete;

// 操作日志状态字典翻译
const statusFormat = (row: any) => {
  return proxy.selectDictLabel(state.statusOptions, row.status);
};

// 页面加载时调用
onMounted(() => {
  handleQuery();
  proxy.getDicts("sys_common_status").then((response: any) => {
    state.statusOptions = response?.data || [];
  });
});
</script>

<style>
</style>
