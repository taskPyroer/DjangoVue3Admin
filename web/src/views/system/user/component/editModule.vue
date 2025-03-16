<template>
  <div class="system-menu-container">
    <el-dialog v-model="state.isShowDialog" :before-close="handleBeforeClose" width="769px" center>
      <template #header>
        <div style="font-size: large"
             v-drag="['.system-menu-container .el-dialog', '.system-menu-container .el-dialog__header']">{{ title }}
        </div>
      </template>
      <el-form
          ref="ruleFormRef"
          :model="state.ruleForm"
          :rules="state.ruleRules"
          label-width="100px"
      >
        <el-row :gutter="35">
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="用户昵称" prop="nickname">
              <el-input v-model="state.ruleForm.nickname" placeholder="请输入用户昵称"
              />
            </el-form-item>
          </el-col>
          <el-col v-if="state.ruleForm.id == undefined" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="用户名称" prop="username">
              <el-input v-model="state.ruleForm.username" placeholder="请输入用户名称"/>
            </el-form-item>
          </el-col>
          <el-col v-if="state.ruleForm.id == undefined" :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="用户密码" prop="password">
              <el-input v-model="state.ruleForm.password" placeholder="请输入用户密码" type="password"/>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="手机号码" prop="phone">
              <el-input v-model="state.ruleForm.phone" placeholder="请输入手机号码" maxlength="11"/>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="state.ruleForm.email" placeholder="请输入邮箱" maxlength="50"/>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="用户性别" prop="gender">
              <el-select v-model="state.ruleForm.gender" placeholder="请选择">
                <el-option
                    v-for="dict in state.sexOptions"
                    :key="dict.dict_value"
                    :label="dict.dict_label"
                    :value="dict.dict_value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="角色">
              <el-select v-model="state.roleIds" multiple placeholder="请选择">
                <el-option
                    v-for="item in state.roleOptions"
                    :key="item.id"
                    :label="item.role_name"
                    :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="归属部门" prop="deptId">
              <el-cascader
                  v-model="state.ruleForm.dept"
                  :options="state.deptOptions"
                  :props="{
                  label: 'dept_name',
                  value: 'id',
                  checkStrictly: true,
                  emitPath: false,
                }"
                  class="w100"
                  clearable
                  filterable
                  placeholder="请选择归属部门"
                  :show-all-levels="false"
              ></el-cascader>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="岗位">
              <el-select v-model="state.postIds" multiple placeholder="请选择">
                <el-option
                    v-for="item in state.postOptions"
                    :key="item.id"
                    :label="item.post_name"
                    :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="状态">
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
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="超级管理员">
              <el-switch
                  v-model="isSuperuser"
                  class="ml-2"
                  inline-prompt
                  style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                  active-text="Y"
                  inactive-text="N"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="后台登录权限">
              <el-switch
                  v-model="isStaff"
                  class="ml-2"
                  inline-prompt
                  style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
                  active-text="Y"
                  inactive-text="N"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
            <el-form-item label="备注">
              <el-input
                  v-model="state.ruleForm.remark"
                  type="textarea"
                  placeholder="请输入内容"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
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

import {reactive, ref, unref, getCurrentInstance} from "vue";
import {deptTreeSelect} from "@/api/system/dept";
import {updateUser, addUser, getUser} from "@/api/system/user";
import {ElMessage} from "element-plus";
import {getAllRoles} from "@/api/system/role";
import {getAllPosts} from "@/api/system/post";

const props = defineProps({
  title: {
    type: String,
    default: () => "",
  },
})

const {proxy} = getCurrentInstance() as any;
const ruleFormRef = ref<HTMLElement | null>(null);
const isSuperuser = ref(false)
const isStaff = ref(false)
const state = reactive({
  // 是否显示弹出层
  isShowDialog: false,
  handleBeforeClose: false,
  loading: false,
  // 默认密码
  // 性别状态字典
  sexOptions: [],
  // 角色选项
  roleOptions: [],
  // 状态数据字典
  statusOptions: [],
  // 部门树选项
  deptOptions: [],
  // 岗位选项
  postOptions: [],
  ruleForm: {
    id: undefined, // 用戶ID
    username: "", // 用戶名称
    nickname: "", // 用戶昵称
    dept: "", // 部门ID
    role: [], // 角色ID
    post: [], // 岗位ID
    phone: "", // 手机号
    email: "", // 邮箱
    status: "", //用户状态
    password: undefined, // 用户密码
    avatar: "", // 用户头像
    gender: "", // 性别
    remark: "", // 备注
    is_superuser: false, // 是否超级管理员
    is_staff: false, // 是否有登录后台权限
    postIds: "",
    roleIds: "",
  },
  postIds: [],
  roleIds: [],
  // 显示状态数据字典
  isHideOptions: [],
  // 菜单类型数据字典
  menuTypeOptions: [],
  // 数字是否数据字典
  yesOrNoOptions: [],
  // 菜单树选项
  menuOptions: [],
  // 表单校验
  ruleRules: {
    username: [
      {required: true, message: "用户名称不能为空", trigger: "blur"},
    ],
    nickname: [
      {required: true, message: "用户昵称不能为空", trigger: "blur"},
    ],
    password: [
      {required: true, message: "用户密码不能为空", trigger: "blur"},
    ],
    email: [
      {
        type: "email",
        message: "'请输入正确的邮箱地址",
        trigger: ["blur", "change"],
      },
    ],
    phone: [
      {
        required: true,
        pattern: /^1[3|4|5|6|7|8|9][0-9]\d{8}$/,
        message: "请输入正确的手机号码",
        trigger: "blur",
      },
    ],
  },
});

// 打开弹窗
const openDialog = (row: any) => {
  if (row && row.id && row.id != undefined && row.id != 0) {
    getUser(row.id).then((response: any) => {
      state.ruleForm = response.data.data;
      state.postIds = response.data.data.post
      state.roleIds = response.data.data.role
      state.ruleForm.password = undefined
      isSuperuser.value = state.ruleForm.is_superuser
      isStaff.value = state.ruleForm.is_staff
    });
  } else {
    state.ruleForm = JSON.parse(JSON.stringify(row));
  }

  getDeptTreeSelect();
  state.isShowDialog = true;
  state.loading = false;
  // 查询所有的角色名称
  getAllRoles().then((response: any) => {
    state.roleOptions = response.data.roles;
  })
  // 查询所有的岗位名称
  getAllPosts().then((response: any) => {
    state.postOptions = response.data.posts;
  })
  // 查询显示性別数据字典
  proxy.getDicts("sys_user_sex").then((response: any) => {
    state.sexOptions = response.data.data;
  });
  // 查询显示狀態数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
  });
};
// 关闭弹窗
const closeDialog = () => {
  state.isShowDialog = false;
  isSuperuser.value = false;
  isStaff.value = false;
  state.postIds = [];
  state.roleIds = [];
};
// 关闭弹窗对话框
const handleBeforeClose = () => {
  closeDialog();
}
// 取消
const onCancel = () => {
  closeDialog();
};
/** 查询部门下拉树结构 */
const getDeptTreeSelect = async () => {
  deptTreeSelect().then((response) => {
    state.deptOptions = response.data;
  });
};

/** 提交按钮 */
const onSubmit = () => {
  const formWrap = unref(ruleFormRef) as any;
  if (!formWrap) return;
  formWrap.validate((valid: boolean) => {
    if (valid) {
      state.ruleForm.post = state.postIds
      state.ruleForm.role = state.roleIds
      state.ruleForm.is_superuser = isSuperuser.value
      state.ruleForm.is_staff = isStaff.value
      state.loading = true;
      if (state.ruleForm.id != undefined) {
        updateUser(state.ruleForm).then(() => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(); // 关闭弹窗
        });
      } else {
        addUser(state.ruleForm).then(() => {
          ElMessage.success("新增成功");
          state.loading = false;
          closeDialog(); // 关闭弹窗
        });
      }
    }
  });
};

// 头像上传
const handleAvatarSuccess = (file: any) => {
  //   state.imageUrl = URL.createObjectURL(file.raw);
};
// 头像上传前校验
const beforeAvatarUpload = (file: any) => {
  const isJPG = file.type === "image/jpeg";
  const isLt2M = file.size / 1024 / 1024 < 2;

  if (!isJPG) {
    ElMessage.error("上传头像图片只能是 JPG 格式!");
  }
  if (!isLt2M) {
    ElMessage.error("上传头像图片大小不能超过 2MB!");
  }
  return isJPG && isLt2M;
};

defineExpose({
  openDialog,
});

</script>
<style scoped lang="scss">
.updateUser {
  height: 100%;
  overflow: auto;
  padding-bottom: 53px;
  width: 600px;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 108px;
  height: 108px;
  margin: 8px;
  line-height: 108px;
  border-radius: 4px;
  text-align: center;
  background-color: #fafafa;
  border: 1px dashed #d9d9d9;
}

.avatar {
  width: 108px;
  height: 108px;
  margin: 8px;
  border-radius: 4px;
  display: block;
}
</style>
