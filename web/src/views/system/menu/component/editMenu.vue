<template>
  <div class="system-menu-container">
    <el-dialog v-model="isShowDialog" width="769px" center>
      <template #header>
        <div
          style="font-size: large"
          v-drag="[
            '.system-menu-container .el-dialog',
            '.system-menu-container .el-dialog__header',
          ]"
        >
          {{ title }}
        </div>
      </template>
      <el-form :model="ruleForm" :rules="ruleRules" ref="ruleFormRef" label-width="80px">
        <el-row :gutter="35">
          <el-col :span="24">
            <el-form-item label="上级菜单" prop="parentId">
              <el-cascader
                v-model="ruleForm.parent"
                :options="menuOptions"
                class="w100"
                :props="{
                  label: 'menu_name',
                  value: 'id',
                  checkStrictly: true,
                  emitPath: false,
                }"
                clearable
                filterable
                placeholder="选择上级菜单"
                :show-all-levels="false"
              ></el-cascader>
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="菜单类型" prop="menuType">
              <el-radio-group v-model="ruleForm.menu_type">
                <el-radio
                  v-for="dict in menuTypeOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="菜单名称" prop="menuName">
              <el-input
                v-model="ruleForm.menu_name"
                placeholder="请输入菜单名称"
                clearable
              ></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="菜单排序" prop="sort">
              <el-input-number
                v-model="ruleForm.sort"
                placeholder="菜单排序"
                clearable
              ></el-input-number>
            </el-form-item>
          </el-col>

          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-form-item label="菜单图标" prop="icon">
              <IconSelector
                placeholder="请输入菜单图标"
                v-model="ruleForm.icon"
                type="all"
              />
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-row :gutter="8">
              <el-col :span="22">
                <el-form-item label="权限标识" prop="permission">
                  <el-input
                    v-model="ruleForm.permission"
                    placeholder="路由权限标识"
                    clearable
                    :disabled="ruleForm.menu_type == 'M' ? true : false"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-tooltip content="路由权限标识（多个请用逗号隔开）" placement="top">
                  <i class="fa fa-exclamation-circle ml10 mt10"></i>
                </el-tooltip>
              </el-col>
            </el-row>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-row :gutter="8">
              <el-col :span="22">
                <el-form-item label="组件地址">
                  <el-input
                    v-model="ruleForm.component"
                    placeholder="组件地址"
                    clearable
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-alert title="若是目录以下有菜单，直接填写Layout，否则填写src/views下的文件夹地址，如/xx/xx/index" type="info" show-icon/>
            </el-row>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-row :gutter="8">
              <el-col :span="22">
                <el-form-item label="路由地址">
                  <el-input
                    v-model="ruleForm.path"
                    placeholder="请输入路由地址"
                    clearable
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-alert title="浏览器中url的地址，请以/开头，要和页面name保持一致:例如 /system/role" type="info" show-icon/>
            </el-row>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
            <el-form-item label="菜单状态" prop="status">
              <el-radio-group v-model="ruleForm.status">
                <el-radio
                  v-for="dict in statusOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-form-item label="是否隐藏">
              <el-radio-group v-model="ruleForm.is_hide">
                <el-radio
                  v-for="dict in isHideOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-form-item label="是否缓存">
              <el-radio-group v-model="ruleForm.is_keep_alive">
                <el-radio
                  v-for="dict in yesOrNoOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-row :gutter="8">
              <el-col :span="22">
                <el-form-item label="是否固定">
                  <el-radio-group v-model="ruleForm.is_affix">
                    <el-radio
                      v-for="dict in yesOrNoOptions"
                      :key="dict.dict_value"
                      :label="dict.dict_value"
                      >{{ dict.dict_label }}
                    </el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <el-tooltip
                  content="是否要固定到tag头部"
                  placement="top"
                  v-if="ruleForm.menu_type != 'F'"
                >
                  <i class="fa fa-exclamation-circle ml10 mt10"></i>
                </el-tooltip>
              </el-col>
            </el-row>
          </el-col>

          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-form-item label="是否内嵌">
              <el-radio-group v-model="ruleForm.is_iframe">
                <el-radio
                  v-for="dict in yesOrNoOptions"
                  :key="dict.dict_value"
                  :label="dict.dict_value"
                  >{{ dict.dict_label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col
            :xs="24"
            :sm="12"
            :md="12"
            :lg="12"
            :xl="12"
            v-if="ruleForm.menu_type != 'F'"
          >
            <el-form-item label="链接地址">
              <el-input
                v-model="ruleForm.is_link"
                placeholder="外链/内嵌时链接地址（http:xxx.com）"
                :clear="clear"
                clearable
              >
              </el-input>
            </el-form-item>
          </el-col>

          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
            <el-form-item label="备注">
              <el-input
                v-model="ruleForm.remark"
                placeholder="请输入备注内容"
                clearable
                type="textarea"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
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

<script setup lang="ts" name="editMenu">
import { reactive, toRefs, ref, unref, getCurrentInstance } from "vue";
import IconSelector from "@/components/iconSelector/index.vue";
import { treeselect, updateMenu, addMenu } from "@/api/system/menu";
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
    menu_name: "",
    menu_type: "",
    parent: undefined as any,
    component: "",
    path: "",
    sort: 1,
    status: "",
    title: "",
    icon: "",
    is_hide: "",
    is_keep_alive: "",
    is_affix: "",
    is_link: "",
    is_iframe: "",
    permission: "",
    remark: "",
  },
  isHideOptions: [] as any[],
  statusOptions: [] as any[],
  menuTypeOptions: [] as any[],
  yesOrNoOptions: [] as any[],
  menuOptions: [] as any[],
  ruleRules: {
    menu_name: [{ required: true, message: "菜单名称不能为空", trigger: "blur" }],
    parent: [{ required: true, message: "父菜单不能为空", trigger: "blur" }],
    menu_type: [{ required: true, message: "菜单类型不能为空", trigger: "blur" }],
    status: [{ required: true, message: "菜单状态不能为空", trigger: "blur" }],
    sort: [{ required: true, message: "菜单顺序不能为空", trigger: "blur" }],
  },
});

const {
  isShowDialog,
  loading,
  ruleForm,
  isHideOptions,
  statusOptions,
  menuTypeOptions,
  yesOrNoOptions,
  menuOptions,
  ruleRules,
} = toRefs(state);

// 打开弹窗
const openDialog = (row: any) => {
  state.ruleForm = JSON.parse(JSON.stringify(row));
  state.isShowDialog = true;
  state.loading = false;
  // 查询显示状态数据字典
  proxy.getDicts("sys_show_hide").then((response: any) => {
    state.isHideOptions = response.data.data;
  });
  // 查询菜单状态数据字典
  proxy.getDicts("sys_yes_no").then((response: any) => {
    state.statusOptions = response.data.data;
  });
  // 查询菜单类型数据字典
  proxy.getDicts("sys_menu_type").then((response: any) => {
    state.menuTypeOptions = response.data.data;
  });
  // 查询数字是否数据字典
  proxy.getDicts("sys_num_yes_no").then((response: any) => {
    state.yesOrNoOptions = response.data.data;
  });
  // 查询菜单下拉树结构
  treeselect().then((response: any) => {
    state.menuOptions = [];
    const menu = { id: undefined, menu_name: "主类目", children: [] };
    menu.children = response.data.data;
    state.menuOptions.push(menu);
  });
};

// 关闭弹窗
const closeDialog = (needRefresh: boolean = false) => {
  if (needRefresh) {
    proxy.mittBus.emit("onEditMenuModule", state.ruleForm);
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
      if (state.ruleForm.component == "") {
        if (state.ruleForm.menu_type == "F") {
          state.ruleForm.component = "";
        } else {
          state.ruleForm.component = "Layout";
        }
      }
      state.loading = true;
      if (state.ruleForm.id != undefined && state.ruleForm.id != 0) {
        updateMenu(state.ruleForm).then(() => {
          ElMessage.success("修改成功");
          state.loading = false;
          closeDialog(true);
        }).catch(() => { state.loading = false; });
      } else {
        addMenu(state.ruleForm).then(() => {
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
