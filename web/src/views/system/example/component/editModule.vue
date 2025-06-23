<template>
  <div class="system-example-container">
    <el-dialog v-model="state.isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large" v-drag="['.system-example-container .el-dialog', '.system-example-container .el-dialog__header']">{{title}}</div>
      </template>
      <el-form
        :model="state.ruleForm"
        :rules="state.ruleRules"
        ref="ruleFormRef"
        label-width="80px"
      >
        <el-row :gutter="30">
          <el-col :span="24">
            <el-form-item label="标题" prop="title">
              <el-input
                v-model="state.ruleForm.title"
                placeholder="请输入标题"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="内容" prop="content">
              <el-input
                v-model="state.ruleForm.content"
                type="textarea"
                :rows="4"
                placeholder="请输入内容"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="分类" prop="category">
              <el-input
                v-model="state.ruleForm.category"
                placeholder="请输入分类"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="state.ruleForm.status">
                <el-radio
                  v-for="dict in state.statusOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.loading"
            >保 存</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, unref, getCurrentInstance } from "vue";
import { updateExample, addExample } from "@/api/system/example";
import { ElMessage } from "element-plus";

const props = defineProps({
  title: {
    type: String,
    default: () => "",
  },
})
const { proxy } = getCurrentInstance() as any;
const ruleFormRef = ref<HTMLElement | null>(null);
const state = reactive({
  // 是否显示弹出层
  isShowDialog: false,
  loading: false,
  // 示例对象
  ruleForm: {
    id: 0, // 示例ID
    title: "", // 标题
    content: "", // 内容
    category: "", // 分类
    status: "0", // 状态
  },
  // 状态数据字典
  statusOptions: [],
  // 表单校验
  ruleRules: {
    title: [
      { required: true, message: "标题不能为空", trigger: "blur" },
      { min: 1, max: 100, message: "标题长度在 1 到 100 个字符", trigger: "blur" }
    ],
    content: [
      { required: true, message: "内容不能为空", trigger: "blur" },
    ],
    category: [
      { required: true, message: "分类不能为空", trigger: "blur" },
    ],
    status: [
      { required: true, message: "状态不能为空", trigger: "blur" },
    ],
  },
});
// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));
  // 如果是新增，设置默认值
  if (!state.ruleForm.id) {
    state.ruleForm.status = "0";
  }

  state.isShowDialog = true;
  state.loading = false;
  // 查询状态数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
  });
};

// 关闭弹窗
const closeDialog = (row?: object) => {
  proxy.mittBus.emit("onEditExampleModule", row)
  state.isShowDialog = false;
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
    if (valid) {
      state.loading = true;
      if (state.ruleForm.id != undefined && state.ruleForm.id != 0) {
        // 修改
        updateExample(state.ruleForm).then((response) => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
        }).catch(() => {
          state.loading = false;
        });
      } else {
        // 新增
        addExample(state.ruleForm).then((response) => {
          ElMessage.success("新增成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
        }).catch(() => {
          state.loading = false;
        });
      }
    }
  });
};

// eslint-disable-next-line no-undef
defineExpose({
  openDialog,
});
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>