<template>
  <div class="system-menu-container">
    <el-dialog v-model="isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large" v-drag="['.system-menu-container .el-dialog', '.system-menu-container .el-dialog__header']">{{title}}</div>
      </template>
      <el-form
        :model="ruleForm"
        :rules="ruleRules"
        ref="ruleFormRef"
        label-width="80px"
      >
        <el-form-item label="字典类型">
          <el-input v-model="ruleForm.dict_type" :disabled="true" />
        </el-form-item>
        <el-form-item label="数据标签" prop="dictLabel">
          <el-input v-model="ruleForm.dict_label" placeholder="请输入数据标签" />
        </el-form-item>
        <el-form-item label="数据键值" prop="dictValue">
          <el-input v-model="ruleForm.dict_value" placeholder="请输入数据键值" />
        </el-form-item>
        <el-form-item label="显示排序" prop="dictSort">
          <el-input-number
            v-model="ruleForm.sort"
            controls-position="right"
            :min="0"
          />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="ruleForm.status">
            <el-radio
              v-for="dict in statusOptions"
              :key="dict.dictValue"
              :label="dict.dictValue"
              >{{ dict.dictLabel }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="ruleForm.remark"
            type="textarea"
            placeholder="请输入内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="loading">编 辑</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts" name="editDictItem">
import { reactive, toRefs, ref, unref, getCurrentInstance } from "vue";
import { addData, updateData } from "@/api/system/dict/data";
import { ElMessage } from "element-plus";

defineProps({
  title: {
    type: String,
    default: () => "",
  },
});

const { proxy } = getCurrentInstance() as any;
const ruleFormRef = ref<HTMLElement | null>(null);
const state = reactive({
  isShowDialog: false,
  loading: false,
  ruleForm: {
    id: 0,
    dict_type: "",
    dict_label: "",
    dict_value: "",
    sort: 0,
    status: "",
    remark: "",
  },
  statusOptions: [
    { dictValue: "0", dictLabel: "正常" },
    { dictValue: "1", dictLabel: "禁用" }
  ],
  deptOptions: [],
  ruleRules: {
    dict_label: [{ required: true, message: "数据标签不能为空", trigger: "blur" }],
    dict_value: [{ required: true, message: "数据键值不能为空", trigger: "blur" }],
    sort: [{ required: true, message: "数据顺序不能为空", trigger: "blur" }]
  },
});

const { isShowDialog, loading, ruleForm, statusOptions, ruleRules } = toRefs(state);

// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));
  state.ruleForm.dict_type = row.dict_type;
  state.isShowDialog = true;
  state.loading = false;
};

// 关闭弹窗
const closeDialog = (needRefresh: boolean = false) => {
  if (needRefresh) {
    proxy.mittBus.emit("onEditDictItemModule", state.ruleForm);
  }
  state.isShowDialog = false;
};

// 取消
const onCancel = () => {
  closeDialog(false);
};

// 保存
const onSubmit = () => {
  const formWrap = unref(ruleFormRef) as any;
  if (!formWrap) return;
  formWrap.validate((valid: boolean) => {
    if (valid) {
      state.loading = true;
      if (state.ruleForm.id != undefined && state.ruleForm.id != 0) {
        updateData(state.ruleForm).then(() => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(true);
        }).catch(() => { state.loading = false; });
      } else {
        addData(state.ruleForm).then(() => {
          ElMessage.success("新增成功");
          state.loading = false;
          closeDialog(true);
        }).catch(() => { state.loading = false; });
      }
    }
  });
};

defineExpose({
  openDialog,
});
</script>
