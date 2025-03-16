<template>
  <div class="system-user-container app-container">
    <el-card shadow="always">
      <!-- 查询 -->
      <el-form
          :model="state.queryParams"
          ref="queryForm"
          :inline="true"
      >
        <el-form-item label="关键词" prop="keyword">
          <el-input
              size="default"
              placeholder="请输入关键词模糊查询"
              clearable
              @keyup.enter="handleQuery"
              style="width: 180px"
              v-model="state.queryParams.keyword"
          />
        </el-form-item>
        <el-form-item label="请求地址" prop="num_lines">
          <el-select
              v-model="state.queryParams.num_lines"
              placeholder="请选择查看日志行数"
              clearable
              style="width: 180px"
          >
            <el-option
                v-for="dict in state.numLinesOptions"
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
          <span class="card-header-text">系统日志</span>
        </div>
      </template>
      <el-tabs type="border-card" v-model="state.activeTab" @tab-click="labelSwitching">
        <el-tab-pane label="server.log" name="server">
          <el-scrollbar class="log-content" style="height: 600px;">
            <pre v-html="state.logContent"></pre>
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane label="error.log" name="error">
          <el-scrollbar class="log-content" style="height: 600px;">
            <pre v-html="state.logContent"></pre>
          </el-scrollbar>
        </el-tab-pane>
      </el-tabs>
    </el-card>

  </div>
</template>

<script lang="ts" setup name="Systemlog">
import {reactive, onMounted} from "vue";
import SvgIcon from "@/components/svgIcon/index.vue";
import {SystemReadLogs} from "@/api/log/oper";

const state = reactive({
  activeTab: "server",
  // 遮罩层
  loading: true,
  // 列表表格数据
  logContent: "",
  // 查询参数
  queryParams: {
    type_log: "server",
    num_lines: undefined,
    keyword: undefined,
  },
  numLinesOptions : [
    {'dict_value': 10, 'dict_label': '近10行'},
    {'dict_value': 50, 'dict_label': '近50行'},
    {'dict_value': 100, 'dict_label': '近100行'},
    {'dict_value': 500, 'dict_label': '近500行'},
  ]
});

/** 查询日志列表 */
const handleQuery = () => {
  state.loading = true;
  SystemReadLogs(state.queryParams).then(
      (response) => {
        let logContent = response.data; // 获取到的内容
        // 定义替换规则
        const replacements = [
          { pattern: /\[INFO\]/gi, replacement: '<span class="highlight-info">[INFO]</span>' },
          { pattern: /\[ERROR\]/gi, replacement: '<span class="highlight-error">[ERROR]</span>' },
          { pattern: /(\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\])/gi, replacement: '<span class="highlight-datetime">$1</span>' }
        ];

        // 对每个替换规则执行替换操作
        for (const { pattern, replacement } of replacements) {
          logContent = logContent.replace(pattern, replacement);
        }
        state.logContent = logContent;
        state.loading = false;
      }
  );
};

/** 重置按钮操作 */
const resetQuery = () => {
  state.queryParams.num_lines = undefined;
  state.queryParams.keyword = undefined;
  handleQuery();
};
// 存储标签页信息的变量

const labelSwitching = (tab: any) => {
  state.logContent = ''
  state.queryParams.type_log = tab.props.name
  handleQuery();
}

/** 页面加载时调用 */
onMounted(() => {
  // 查询列表数据信息
  handleQuery();

});
</script>

<style>
.log-content {
  background-color: #272821;
  color: white;
  font-size: 16px;
  white-space: pre-wrap;
}


.log-content .highlight-info {
  color: #67c23a;
  font-weight: bold;
}

.log-content .highlight-error {
  color: red;
  font-weight: bold;
}


.log-content .highlight-datetime {
  color: cyan;
  font-weight: bold;
}
</style>
