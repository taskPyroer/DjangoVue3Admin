<template>
  <el-row :gutter="20">
    <el-col :span="6" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}"
            v-if="!dataList.is_windows">
      <div :style="{height:height}" class="space-inner">
        <div class="card">
          <div class="space-header">
            <div class="space-header-title">负载状态</div>
          </div>
          <div class="space-main">
            <div class="space-main-up">
              <el-progress type="circle" :percentage="dataList.load_average.percent" :stroke-width="8" :color="colors"/>
              <div class="space-main-up-cpu">
                <span>最近1分钟平均负载：{{ dataList.load_average.one }}</span>
                <span>最近5分钟平均负载：{{ dataList.load_average.five }}</span>
                <span>最近15分钟平均负载：{{ dataList.load_average.fifteen }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="6" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}">
      <div :style="{height:height}" class="space-inner">
        <div class="card">
          <div class="space-header">
            <div class="space-header-title">CPU使用率</div>
          </div>
          <div class="space-main">
            <div class="space-main-up">
              <el-progress type="circle" :percentage="dataList.cpu[0]" :stroke-width="8" :color="colors"/>
              <div class="space-main-up-cpu">
                <span>CPU型号：{{ dataList.cpu[3] }}</span>
                <span>物理CPU：{{ dataList.cpu[5] }}颗</span>
                <span>物理核心：{{ dataList.cpu[5] * dataList.cpu[4] }}个</span>
                <span>逻辑核心：{{ dataList.cpu[1] }}个</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="6" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}">
      <div :style="{height:height}" class="space-inner">
        <div class="card">
          <div class="space-header">
            <div class="space-header-title">内存使用率</div>
          </div>
          <div class="space-main">
            <div class="space-main-up">
              <el-progress type="circle" :percentage="dataList.mem.percent" :stroke-width="8" :color="colors"/>
              <div class="space-main-up-cpu">
                <span>总共内存：{{ dataList.mem.total }}GB</span>
                <span>已用内存：{{ dataList.mem.used }}GB</span>
                <span>剩余内存：{{ dataList.mem.free }}GB</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-col>
    <el-col :span="6" :xs="{span: 24}" :sm="{span: 24}" :md="{span: 12}" :lg="{span: 6}" :xl="{span: 6}"
            v-for="(item,index) in dataList.disk">
      <div :style="{height:height}" class="space-inner">
        <div class="card">
          <div class="space-header">
            <div class="space-header-title">硬盘使用率： {{ item.path }}</div>
          </div>
          <div class="space-main">
            <div class="space-main-up">
              <el-progress type="circle" :percentage="parseFloat(item.size[3])" :stroke-width="8" :color="colors"/>
              <div class="space-main-up-cpu">
                <span>总共大小：{{ item.size[0] }}</span>
                <span>已用大小：{{ item.size[1] }}</span>
                <span>剩余大小：{{ item.size[2] }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-col>
  </el-row>

</template>

<script>
export default {
  name: "StatusCard",
  data() {
    return {
      dataList: {
        cpu: [0, 0, [0, 0, 0, 0], "Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz * 1", 0, 1],
        disk: [{path: "", size: ["0GB", "0GB", "0GB", 0], inodes: false}],
        is_windows: true,
        load_average: {one: 0, five: 0, fifteen: 0, max: 0, limit: 0, safe: 0, percent: 0},
        mem: {percent: 0, total: 0, free: 0, used: 0},
        system: "Windows 10 Pro (build 16299) x64 (Py3.9.8)",
        time: "0天"
      },
      colors: [
        {color: '#5cb87a', percentage: 30},
        {color: '#1989fa', percentage: 70},
        // { color: '#6f7ad3', percentage: 65 },
        {color: '#e6a23c', percentage: 80},
        {color: '#f56c6c', percentage: 90},
      ],
      load_config: [{
        title: '运行堵塞',
        percentage: 90,
        color: '#dd2f00'
      }, {
        title: '运行缓慢',
        percentage: 80,
        color: '#ff9900'
      }, {
        title: '运行正常',
        percentage: 70,
        color: '#20a53a'
      }, {
        title: '运行流畅',
        percentage: 30,
        color: '#20a53a'
      }],
    }
  },
  mounted() {
    this.dataList = this.modelValue
  },
  props: {
    loading: {
      type: Boolean,
      default: true
    },
    count: {
      type: Number,
      default: 1,
    },
    rows: {
      type: Number,
      default: 4,
    },
    animated: {
      type: Boolean,
      default: true,
    },
    modelValue: {
      type: Object,
      default: {
        cpu: [0, 0, [0, 0, 0, 0], "Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz * 1", 0, 1],
        disk: [{path: "", size: ["0GB", "0GB", "0GB", 0], inodes: false}],
        is_windows: true,
        load_average: {one: 0, five: 0, fifteen: 0, max: 0, limit: 0, safe: 0, percent: 0},
        mem: {percent: 0, total: 0, free: 0, used: 0},
        system: "Windows 10 Pro (build 16299) x64 (Py3.9.8)",
        time: "0天"
      }
    },
    height: {
      type: Number,
      default: 200,
    }
  },
  watch: {
    modelValue: function (nval) {
      this.dataList = nval;
    },
    dataList: function (nval) {
      this.$emit('update:modelValue', nval);
    }
  },
}
</script>

<style scoped>
.space-inner {
}

.card {
  background: var(--el-bg-color);
  box-shadow: var(--el-box-shadow-light);
  border: 1px solid var(--el-border-color-light);
}

.space-header {
  border-bottom: 1px solid var(--el-color-info-light-7);
  font-size: 14px;
  padding: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.space-header-title {
  padding: 8px 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  margin-left: 10px;
}

.space-main {
  padding: 20px;
}

.space-main-up {
  display: flex;
  align-items: center;
  column-gap: 20px;
  /*justify-content: space-around;*/
}

.space-main-up-cpu {
  font-size: 12px;
  display: flex;
  flex-direction: column;
  line-height: 20px;
  /*width: 200px;*/
  color: #666666;
}

::v-deep(.el-col) {
  margin-bottom: 11px;
}
</style>
