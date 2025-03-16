<template>
  <div class="system-notice-container">
    <el-dialog title="信息内容" v-model="state.conOpen" width="769px" center>
      <el-descriptions :column="2" border>
        <el-descriptions-item width="100" label="通知标题">
          {{ state.content.title }}
        </el-descriptions-item>
        <el-descriptions-item width="100" label="通知类型">
          {{ noticeTypeFormat(state.content.target_type) }}
        </el-descriptions-item>
        <el-descriptions-item width="100" label="通知内容">
          <Editor v-model:get-html="state.content.content" :disable="true"></Editor>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup name="viewModule">
import Editor from '@/components/editor/index.vue';
import {getCurrentInstance, reactive} from "vue";
import {getNotice} from "@/api/system/notice";

const {proxy} = getCurrentInstance() as any;
const state = reactive({
  noticeTypeOptions: [],
  conOpen: false,
  content: {
    target_type: undefined,
    title: undefined,
    content: undefined,
  },
});
const openDialog = (row: any, noticeTypeOptions:any) => {
  getNotice(row.id).then((response: any) => {
    state.content = response.data;
  })
  state.conOpen = true
  state.noticeTypeOptions = noticeTypeOptions;
};
// 定时任务状态定时任务翻译
const noticeTypeFormat = (row: any) => {
  return proxy.selectDictLabel(state.noticeTypeOptions, row);
};

defineExpose({
  openDialog,
});

</script>

<style scoped>
.span {
  color: #ff7f0e;
}
</style>
