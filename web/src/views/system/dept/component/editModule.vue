<template>
  <div class="system-menu-container">
    <el-dialog v-model="state.isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large" v-drag="['.system-menu-container .el-dialog', '.system-menu-container .el-dialog__header']">{{title}}</div>
      </template>
      <el-form
        :model="state.ruleForm"
        :rules="state.ruleRules"
        ref="ruleFormRef"
        label-width="80px"
      >
        <el-row :gutter="30">
          <el-col :span="24" >
            <el-form-item label="上级部门" prop="parentId">
              <el-cascader
                v-model="state.ruleForm.parent"
                :options="state.deptOptions"
                class="w100"
                :props="{
                  value: 'id',
                  label: 'dept_name',
                  checkStrictly: true,
                  emitPath: false,
                }"
                clearable
                placeholder="选择上级部门"
                :show-all-levels="false"
              ></el-cascader>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="部门名称" prop="dept_name">
              <el-input
                v-model="state.ruleForm.dept_name"
                placeholder="请输入部门名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="负责人">
              <el-input
                v-model="state.ruleForm.leader"
                placeholder="请输入负责人"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="联系电话" prop="phone">
              <el-input
                v-model="state.ruleForm.phone"
                placeholder="请输入联系电话"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="联系邮箱" prop="email">
              <el-input
                v-model="state.ruleForm.email"
                placeholder="请输入邮箱"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="部门状态" prop="status">
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
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12" >
            <el-form-item label="部门排序" prop="sort">
              <el-input-number
                v-model="state.ruleForm.sort"
                placeholder="部门排序"
                clearable
                controls-position="right"
                :min="0"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.loading"
            >编 辑</el-button
          >
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, unref, getCurrentInstance } from "vue";
import { deptTreeSelect, updateDept, addDept } from "@/api/system/dept";
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
  // 部门对象
  ruleForm: {
    id: 0, // 部门ID
    dept_name: "", // 部门名称
    parent: 0, // 父部门ID
    sort: 0, // 部门排序
    status: "", //部门状态
    leader: "", // 部门负责人
    phone: "", // 联系电话
    email: "", // 邮箱
  },
  // 部门状态数据字典
  statusOptions: [],
  // 部门树选项
  deptOptions: [],
  // 表单校验
  ruleRules: {
    dept_name: [
      { required: true, message: "部门名称不能为空", trigger: "blur" },
    ],
    parent: [
      { required: true, message: "父部门不能为空", trigger: "blur" },
    ],
    status: [
      { required: true, message: "部门状态不能为空", trigger: "blur" },
    ],
    sort: [
      { required: true, message: "部门顺序不能为空", trigger: "blur" },
    ],
    email: [
      {
        type: "email",
        message: "'请输入正确的邮箱地址",
        trigger: ["blur", "change"]
      }
    ],
    phone: [
      {
        pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
        message: "请输入正确的手机号码",
        trigger: "blur"
      }
    ]
  },
});
// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));

  state.isShowDialog = true;
  state.loading = false;
  // 查询部门状态数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
  });

  // 查询部门下拉树结构
  deptTreeSelect().then((response: any) => {
    state.deptOptions = [];
    const dept = { id: 0, dept_name: '主类目', children: [] }
    dept.children = response.data
    state.deptOptions.push(dept)
  });
};

// 关闭弹窗
const closeDialog = (row?: object) => {
  proxy.mittBus.emit("onEditDeptModule",row)
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
        // eslint-disable-next-line no-unused-vars
        updateDept(state.ruleForm).then((response) => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
        });
      } else {
        // eslint-disable-next-line no-unused-vars
        addDept(state.ruleForm).then((response) => {
          ElMessage.success("新增成功");
          state.loading = false;
          closeDialog(state.ruleForm); // 关闭弹窗
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
