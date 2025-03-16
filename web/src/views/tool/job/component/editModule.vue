<template>
  <div class="system-job-container">
    <el-dialog v-model="state.isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large"
             v-drag="['.system-job-container .el-dialog', '.system-job-container .el-dialog__header']">{{ title }}
        </div>
      </template>
      <el-form
          :model="state.ruleForm"
          :rules="state.ruleRules"
          ref="ruleFormRef"
          label-width="100px"
      >
        <el-form-item label="任务名称：" prop="name">
          <el-input v-model="state.ruleForm.name" placeholder="请输入任务名称"/>
        </el-form-item>
        <el-form-item label="任务类型：" prop="type">
          <el-tooltip effect="dark" content='不支持编辑任务类型' placement="top-start" style="display: flex; align-items: center;">
            <el-icon>
              <question-filled/>
            </el-icon>
          </el-tooltip>
          <el-radio-group v-model="state.ruleForm.type">
            <el-radio-button :label="0" :disabled="state.isDisabled">间隔任务</el-radio-button>
            <el-radio-button :label="1" :disabled="state.isDisabled">周期任务</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="执行时间：" v-if="state.ruleForm.type == 0" class="is-required">
          <el-row>
            每隔
            <el-input-number
                v-model="state.interval.every"
                :min="0"
                style="margin: 0 5px 0 5px"
            ></el-input-number>
            <el-select v-model="state.interval.period" style="width: 150px">
              <el-option
                  v-for="item in state.intervalList"
                  :key=item.id
                  :label=item.name
                  :value=item.id
              ></el-option>
            </el-select>
          </el-row>
        </el-form-item>
        <el-form-item label="执行时间：" prop="crontab" v-if="state.ruleForm.type == 1" class="is-required">
          <el-input
              v-model="state.ruleForm.crontab"
              placeholder="* * * * *"
          >
            <template #append>
              <el-button type="primary" @click="togglePopover(true)">生成表达式
                <el-icon>
                  <Clock/>
                </el-icon>
              </el-button>
            </template>
          </el-input>
          <el-alert type="info">
            <template #default>
              <img src="@/assets/cronexpress.png" style="width: 100%;">
            </template>
          </el-alert>
          <el-drawer v-model="state.cronPopover" title="cron表达式辅助工具" size="40%" :show-close="false">
            <cronExpression
                @change="changeCron"
                @close="togglePopover(false)"
                max-height="400px"
                i18n="cn"
            ></cronExpression>
          </el-drawer>
        </el-form-item>
        <el-form-item label="执行方法：" prop="task">
          <el-select v-model="state.ruleForm.task" placeholder="请输入或选择" allow-create filterable clearable
                     style="width: 100%">
            <el-option
                v-for="item in state.taskList"
                :key="item.label"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
          <el-alert title="Celery任务调用示例：app_crontab.tasks.cron_job_add" type="info" show-icon/>
        </el-form-item>
        <el-form-item label="任务参数：" prop="kwargs">
          <el-tooltip effect="dark" content='参数若为空则填置空,需要传递参数则直接在数组写值即可：如{"x": 5, "y": 6}'
                      placement="top-start" style="display: flex; align-items: center;">
            <el-icon>
              <question-filled/>
            </el-icon>
          </el-tooltip>
          <el-input v-model="state.ruleForm.kwargs" placeholder="请输入任务参数" style="flex: 1;"/>
        </el-form-item>
        <el-form-item label="一次性任务：" prop="one_off">
          <el-switch
              v-model="state.ruleForm.one_off"
              active-text="是"
              inactive-text="否"
              active-color="#13ce66"
              inactive-color="#ff4949">
          </el-switch>
        </el-form-item>
        <el-form-item label="状态：" prop="enabled">
          <el-switch
              v-model="state.ruleForm.enabled"
              active-text="正常"
              inactive-text="停止"
              active-color="#13ce66"
              inactive-color="#ff4949">
          </el-switch>
        </el-form-item>
        <el-form-item label="备注：" prop="description">
          <el-input v-model="state.ruleForm.description" type="textarea" :rows="2"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.loading">编 辑</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {reactive, toRefs, ref, unref, getCurrentInstance} from "vue";
import {addJob, listTask, updateJob} from "@/api/tool/job";
import {ElMessage} from "element-plus";
import cronExpression from "./cronExpression.vue";

const props = defineProps({
  title: {
    type: String,
    default: () => "",
  },
})

const {proxy} = getCurrentInstance() as any;
const ruleFormRef = ref<HTMLElement | null>(null);
const state = reactive({
  // 是否显示弹出层
  isShowDialog: false,
  loading: false,
  // 表单参数对象
  ruleForm: {
    id: 0, // 定时任务ID
    name: "", // 定时任务名称
    kwargs: "", //调用方法 传参
    type: 0,// 任务类型
    crontab: '',
    task: '',
    one_off: false,
    enabled: false,
    description: '',
    interval: {}
  },
  interval: {
    every: null,
    period: null,
  },
  // 任务组名字典
  taskList: [],
  // 表单校验
  ruleRules: {
    name: [
      {required: true, message: "任务名称不能为空", trigger: "blur"},
    ],
    task: [
      {required: true, message: '请输入celery任务方法', trigger: 'blur'}
    ],
    type: [
      {required: true, message: '请选择任务类型', trigger: 'blur'}
    ],
  },
  // 间隔类型
  intervalList: [
    {id: 'days', name: '天'},
    {id: 'hours', name: '小时'},
    {id: 'minutes', name: '分钟'},
    {id: 'seconds', name: '秒'},
    {id: 'microseconds', name: '微秒'},
  ],
  cronPopover: false,
  // 是否禁用
  isDisabled: false
});

const changeCron = (val: any) => {
  if (typeof val !== 'string') return false
  state.ruleForm.crontab = val
}

const togglePopover = (bol: any) => {
  state.cronPopover = bol
}

// 加载任务列表
const getListTask = () => {
  listTask().then((response: any) => {
        state.taskList = response.data.data;
      }
  );
};

// 打开弹窗
const openDialog = (row: any) => {
  getListTask();
  state.ruleForm = JSON.parse(JSON.stringify(row));
  if (state.ruleForm.type == 0){
    state.interval = state.ruleForm.interval;
  }
  state.isShowDialog = true;
  state.loading = false;
  if (state.ruleForm.id > 0){
    state.isDisabled = true;
  }
};

// 关闭弹窗
const closeDialog = (row?: object) => {
  proxy.mittBus.emit("onEditJobModule", row);
  state.isShowDialog = false;
  state.interval = {
    every: null,
    period: null,
  }
  state.isDisabled = false;
};
// 取消
const onCancel = () => {
  closeDialog();
};

// 保存
const onSubmit = () => {
  const formWrap = unref(ruleFormRef) as any;
  if (!formWrap) return;
  formWrap.validate((valid: boolean) => {
    if (state.ruleForm.type === 1) {
      if (state.ruleForm.crontab == "") {
        state.loading = false;
        ElMessage.warning("执行时间不能为空");
        return
      }
    }
    if (state.ruleForm.type === 0) {
      if (state.interval.every == null || state.interval.every == "" || state.interval.period == null || state.interval.period == "") {
        state.loading = false;
        ElMessage.warning("执行时间不能为空");
        return
      }
    }
    if (valid) {
      state.ruleForm = {
        ...state.ruleForm, // 先复制ruleForm原有的属性
        interval: {
          period: state.interval.period,
          every: state.interval.every
        }
      }
      state.loading = true;
      if (state.ruleForm.id != undefined && state.ruleForm.id != 0) {
        updateJob(state.ruleForm).then((response) => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
        });
      } else {
        if (state.ruleForm.kwargs) {
          state.ruleForm.kwargs = JSON.parse(state.ruleForm.kwargs);
        }
        addJob(state.ruleForm).then((response) => {
          ElMessage.success("新增成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
        });
      }
    }
  });
};

defineExpose({
  openDialog,
});
</script>
