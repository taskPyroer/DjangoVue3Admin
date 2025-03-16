<template>
  <div class="system-notice-container">
    <el-dialog v-model="state.isShowDialog" width="769px" center>
      <template #header>
        <div style="font-size: large"
             v-drag="['.system-notice-container .el-dialog', '.system-notice-container .el-dialog__header']">{{ title }}
        </div>
      </template>
      <el-form
          :model="state.ruleForm"
          :rules="state.ruleRules"
          ref="ruleFormRef"
          label-width="100px"
      >
        <el-row class="mb20">
          <el-col :span="24">
            <el-form-item label="信息标题">
              <el-input v-model="state.ruleForm.title" placeholder="请输入信息标题"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row class="mb20">
          <el-col :span="12">
            <el-form-item label="信息类型">
              <el-select v-model="state.ruleForm.target_type" placeholder="请选择">
                <el-option
                    v-for="dict in state.noticeTypeOptions"
                    :key="dict.dict_value"
                    :label="dict.dict_label"
                    :value="dict.dict_value"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item v-if="state.ruleForm.target_type === '0'" label="通知用户">
              <el-select v-model="state.ruleForm.target_user" multiple clearable placeholder="请选择用户" @click="openUserDialog">
                <el-option
                    v-for="item in state.userOptions.data"
                    :key="item.id"
                    :label="item.username"
                    :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-if="state.ruleForm.target_type === '1'" label="通知角色">
              <el-select v-model="state.ruleForm.target_role" multiple clearable placeholder="请选择角色">
                <el-option
                    v-for="item in state.roleOptions"
                    :key="item.id"
                    :label="item.role_name"
                    :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-if="state.ruleForm.target_type === '2'" label="通知部门">
              <el-cascader
                  v-model="state.ruleForm.target_dept"
                  :options="state.deptOptions"
                  class="w100"
                  :props="{
                  label: 'dept_name',
                  value: 'id',
                  multiple: true
                }"
                  clearable
                  placeholder="选择通知部门"
                  :show-all-levels="false"
              ></el-cascader>
            </el-form-item>
          </el-col>
        </el-row>
        <el-col :span="24">
          <el-form-item label="通知内容" prop="content">
            <Editor v-model:get-html="state.ruleForm.content"></Editor>
          </el-form-item>
        </el-col>
        <el-col :span="24">
          <el-form-item label="备注" prop="content">
            <el-input
                v-model="state.ruleForm.remark"
                :autosize="{ minRows: 2, maxRows: 4 }"
                type="textarea"
                placeholder="请输入备注..."
            />
          </el-form-item>
        </el-col>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="onCancel">取 消</el-button>
          <el-button type="primary" @click="onSubmit" :loading="state.loading">确 定</el-button>
        </span>
      </template>
    </el-dialog>

    <!--    用户查询添加弹出框-->
    <el-dialog v-model="state.dialogVisible">
      <el-card shadow="always">
        <!-- 查询-->
        <el-form
            :model="state.userQueryParams"
            ref="queryForm"
            :inline="true"
            label-width="78px"
        >
          <el-form-item label="用户名称" prop="username">
            <el-input
                placeholder="用户名称模糊查询"
                clearable
                @keyup.enter="UserHandleQuery"
                style="width: 240px"
                v-model="state.userQueryParams.search"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" plain @click="UserHandleQuery">
              <SvgIcon name="elementSearch"/>
              搜索
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
      <!-- table columns and data -->
      <el-card class="box-card">
        <template #header>
          <div class="card-header">
            <span class="card-header-text">用户列表</span>
            <div>
              <el-button
                  type="primary"
                  plain
                  :disabled="state.multiple"
                  @click="handleAdd"
              >
                <SvgIcon name="elementPlus"/>
                确定
              </el-button>
            </div>
          </div>
        </template>
        <el-table v-loading="state.userLoading" :data="state.userOptions.data" stripe
                  @selection-change="handleSelectionChange"
                  width="500px" center>
          <el-table-column type="selection" width="45" align="center"/>
          <el-table-column label="用户编号" align="center" prop="id"/>
          <el-table-column label="用户名" prop="username" show-overflow-tooltip></el-table-column>
          <el-table-column prop="phone" label="手机" show-overflow-tooltip></el-table-column>
          <el-table-column prop="dept_name" label="部门名称" show-overflow-tooltip></el-table-column>
        </el-table>
        <div v-show="state.userOptions.total > 0">
          <el-divider></el-divider>
          <el-pagination
              background
              :total="state.userOptions.total"
              :page-sizes="[10, 20, 30]"
              :current-page="state.userQueryParams.page"
              :page-size="state.userQueryParams.pageSize"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="onHandleSizeChange"
              @current-change="onHandleCurrentChange"
          />
        </div>
      </el-card>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref, unref, getCurrentInstance} from "vue";
import {addNotice} from "@/api/system/notice";
import {ElMessage} from "element-plus";
import {deptTreeSelect} from "@/api/system/dept";
import {getAllRoles} from "@/api/system/role";
import {listUser} from "@/api/system/user";
import Editor from '@/components/editor/index.vue';

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
  userLoading: false,
  dialogVisible: false,
  // 查询参数
  queryParams: {
    page: 1,
    pageSize: 10,
    search: undefined,
    status: undefined,
    dept: undefined,
  },
  // 用户查询
  userQueryParams: {
    page: 1,
    pageSize: 10,
    search: undefined,
  },
  // 非单个禁用
  single: true,
  // 非多个禁用
  multiple: true,
  // 选中数组
  userSelectIds: [],
  // 表单参数对象
  ruleForm: {
    id: 0,  // 信息ID
    title: "",    // 信息名称
    target_type: "", // 信息类型
    content: "",     //内容
    remark: "",     //备注
    target_user: [],  // 目标用户
    target_role: [],  // 目标角色
    target_dept: [],  // 目标部门
  },
  // 信息类型字典
  noticeTypeOptions: [],
  // 部门
  deptOptions: [],
  // 角色
  roleOptions: [],
  // 用户
  userOptions: {
    data: [],
    total: 0,
  },
  // 表单校验
  ruleRules: {
    title: [
      {required: true, message: "信息名称不能为空", trigger: "blur"},
    ],
    target_type: [
      {required: true, message: "信息类型不能为空", trigger: "blur",},
    ],
  },
});
// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));

  state.isShowDialog = true;
  state.loading = false;
  // 查询信息类型名字典
  proxy.getDicts("sys_notice_type").then((response: any) => {
    state.noticeTypeOptions = response.data.data;
  });
  getDeptTreeSelect();
  getAllRoleSelect();
};

// 打开用户选择弹窗
const openUserDialog = () => {
  state.dialogVisible = true;
  getUserList();
}

// 分页改变
const onHandleSizeChange = (val: number) => {
  state.queryParams.pageSize = val;
  getUserList();
};

// 分页改变
const onHandleCurrentChange = (val: number) => {
  state.queryParams.page = val;
  getUserList();
};

// 搜索按钮操作
const UserHandleQuery = async () => {
  state.userQueryParams.page = 1;
  await getUserList();
};

// 查询用户列表
const getUserList = async () => {
  state.userLoading = true;
  listUser(state.userQueryParams).then(
      (response: any) => {
        if (response.code != 200) {
          state.userLoading = false;
        }
        state.userOptions.data = response.data.data;
        state.userOptions.total = response.data.total;
        state.userLoading = false;
      }
  );
};

// 确定筛选用户数据
const handleAdd = (row: any) => {
  state.ruleForm.target_user = row.id || state.userSelectIds;
  state.dialogVisible = false;
};

// 查询部门下拉树结构
const getDeptTreeSelect = async () => {
  deptTreeSelect().then((response) => {
    state.deptOptions = response.data;
  });
};

// 查询所有的角色名称
const getAllRoleSelect = async () => {
  getAllRoles().then((response: any) => {
    state.roleOptions = response.data.roles;
  });
}

// 用户多选框选中数据
const handleSelectionChange = (selection: any) => {
  state.userSelectIds = selection.map((item: any) => item.id);
  state.single = selection.length != 1;
  state.multiple = !selection.length;
};

// 关闭弹窗
const closeDialog = (row?: object) => {
  proxy.mittBus.emit("onEditNoticeModule", row);
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
        // 不支持修改已发送的信息
      } else {
        if (state.ruleForm.target_type === '2') {
          // 使用 flat() 方法将嵌套数组展开为一个一维数组
          const flattenedArray = state.ruleForm.target_dept.flat();
          // 使用 Set 来去重，并将其转换为数组
          state.ruleForm.target_dept = [...new Set(flattenedArray)];
        }
        addNotice(state.ruleForm).then(() => {
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
