<template>
  <div class="system-menu-container">
    <el-dialog v-model="isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large"
             v-drag="['.system-menu-container .el-dialog', '.system-menu-container .el-dialog__header']">{{ title }}
        </div>
      </template>
      <el-form
          :model="ruleForm"
          :rules="ruleRules"
          ref="ruleFormRef"
          label-width="80px"
      >
        <el-form-item label="字典名称" prop="dict_name">
          <el-input v-model="ruleForm.dict_name" placeholder="请输入字典名称"/>
        </el-form-item>
        <el-form-item label="字典类型" prop="dict_type">
          <el-input v-model="ruleForm.dict_type" placeholder="请输入字典类型"/>
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

<script setup lang="ts" name="editDictModule">
import {reactive, toRefs, ref, unref, getCurrentInstance} from "vue";
import {addType, updateType} from "@/api/system/dict/type";
import {ElMessage} from "element-plus";

defineProps({
  title: {
    type: String,
    default: () => "",
  },
});

const {proxy} = getCurrentInstance() as any;
const ruleFormRef = ref<HTMLElement | null>(null);
const state = reactive({
  isShowDialog: false,
  loading: false,
  ruleForm: {
    id: 0,
    dict_name: "",
    dict_type: "",
    status: "",
    remark: "",
  },
  statusOptions: [
    { dictValue: "0", dictLabel: "正常" },
    { dictValue: "1", dictLabel: "禁用" }
  ],
  ruleRules: {
    dict_name: [{required: true, message: "字典名称不能为空", trigger: "blur"}],
    dict_type: [{required: true, message: "字典类型不能为空", trigger: "blur"}],
  },
});

const { isShowDialog, loading, ruleForm, statusOptions, ruleRules } = toRefs(state);

// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));
  state.isShowDialog = true;
  state.loading = false;
};

// 关闭弹窗
const closeDialog = (needRefresh: boolean = false) => {
  if (needRefresh) {
    proxy.mittBus.emit("onEditDictTypeModule", state.ruleForm);
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
        updateType(state.ruleForm).then(() => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(true);
        }).catch(() => { state.loading = false; });
      } else {
        addType(state.ruleForm).then(() => {
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
