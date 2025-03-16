<template>
  <div class="vue3-cron-div">
    <el-tabs type="border-card">
      <el-tab-pane>
        <template #label>
          <span><el-icon><Calendar/></el-icon> {{ state.text.Minutes.name }}</span>
        </template>
        <div class="tabBody myScroller" :style="{'max-height': maxHeight}">
          <el-row>
            <el-radio v-model="state.minute.cronEvery" label="1">{{
                state.text.Minutes.every
              }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.minute.cronEvery" label="2"
            >{{ state.text.Minutes.interval[0] }}
              <el-input-number
                  v-model="state.minute.incrementIncrement"
                  :min="1"
                  :max="60"
              ></el-input-number>
              {{ state.text.Minutes.interval[1] }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio class="long" v-model="state.minute.cronEvery" label="3"
            >{{ state.text.Minutes.specific }}
              <el-select
                  multiple
                  v-model="state.minute.specificSpecific"
              >
                <el-option
                    v-for="(val, index) in 60"
                    :key="index"
                    :value="val - 1"
                >{{ val - 1 }}
                </el-option
                >
              </el-select>
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.minute.cronEvery" label="4"
            >{{ state.text.Minutes.cycle[0] }}
              <el-input-number
                  v-model="state.minute.rangeStart"
                  :min="1"
                  :max="60"
              ></el-input-number>
              {{ state.text.Minutes.cycle[1] }}
              <el-input-number
                  v-model="state.minute.rangeEnd"
                  :min="0"
                  :max="59"
              ></el-input-number>
              {{ state.text.Minutes.cycle[2] }}
            </el-radio>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span><el-icon><Calendar/></el-icon> {{ state.text.Hours.name }}</span>
        </template>
        <div class="tabBody myScroller" :style="{'max-height': maxHeight}">
          <el-row>
            <el-radio v-model="state.hour.cronEvery" label="1">{{
                state.text.Hours.every
              }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.hour.cronEvery" label="2"
            >{{ state.text.Hours.interval[0] }}
              <el-input-number
                  v-model="state.hour.incrementIncrement"
                  :min="0"
                  :max="23"
              ></el-input-number>
              {{ state.text.Hours.interval[1] }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio class="long" v-model="state.hour.cronEvery" label="3"
            >{{ state.text.Hours.specific }}
              <el-select multiple v-model="state.hour.specificSpecific">
                <el-option
                    v-for="(val, index) in 24"
                    :key="index"
                    :value="val - 1"
                >{{ val - 1 }}
                </el-option
                >
              </el-select>
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.hour.cronEvery" label="4"
            >{{ state.text.Hours.cycle[0] }}
              <el-input-number
                  v-model="state.hour.rangeStart"
                  :min="0"
                  :max="23"
              ></el-input-number>
              {{ state.text.Hours.cycle[1] }}
              <el-input-number
                  v-model="state.hour.rangeEnd"
                  :min="0"
                  :max="23"
              ></el-input-number>
              {{ state.text.Hours.cycle[2] }}
            </el-radio>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span><el-icon><Calendar/></el-icon> {{ state.text.Day.name }}</span>
        </template>
        <div class="tabBody myScroller" :style="{'max-height': maxHeight}">
          <el-row>
            <el-radio v-model="state.day.cronEvery" label="1">{{
                state.text.Day.every
              }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.day.cronEvery" label="3"
            >{{ state.text.Day.intervalDay[0] }}
              <el-input-number
                  v-model="state.day.incrementIncrement"
                  :min="1"
                  :max="31"
              ></el-input-number>
              {{ state.text.Day.intervalDay[1] }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio class="long" v-model="state.day.cronEvery" label="5"
            >{{ state.text.Day.specificDay }}
              <el-select multiple v-model="state.day.specificSpecific">
                <el-option
                    v-for="(val, index) in 31"
                    :key="index"
                    :value="val"
                >{{ val }}
                </el-option
                >
              </el-select>
            </el-radio>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span><el-icon><Calendar/></el-icon> {{ state.text.Week.name }}</span>
        </template>
        <div class="tabBody myScroller" :style="{'max-height': maxHeight}">
          <el-row>
            <el-radio v-model="state.day.cronEvery" label="1">{{
                state.text.Week.every
              }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.day.cronEvery" label="2"
            >{{ state.text.Day.intervalWeek[0] }}
              <el-input-number
                  v-model="state.week.incrementIncrement"
                  :min="1"
                  :max="7"
              ></el-input-number>
              {{ state.text.Day.intervalWeek[1] }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio class="long" v-model="state.day.cronEvery" label="4"
            >{{ state.text.Day.specificWeek }}
              <el-select multiple v-model="state.week.specificSpecific">
                <el-option
                    v-for="(val, index) in 7"
                    :key="index"
                    :label="state.text.Week.week[val - 1]"
                    :value="
                    ['0', '1', '2', '3', '4', '5', '6'][val - 1]
                  "
                ></el-option>
              </el-select>
            </el-radio>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane>
        <template #label>
          <span><el-icon><Calendar/></el-icon> {{ state.text.Month.name }}</span>
        </template>
        <div class="tabBody myScroller" :style="{'max-height': maxHeight}">
          <el-row>
            <el-radio v-model="state.month.cronEvery" label="1">{{
                state.text.Month.every
              }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.month.cronEvery" label="2"
            >{{ state.text.Month.interval[0] }}
              <el-input-number
                  v-model="state.month.incrementIncrement"
                  :min="0"
                  :max="12"
              ></el-input-number>
              {{ state.text.Month.interval[1] }}
            </el-radio>
          </el-row>
          <el-row>
            <el-radio class="long" v-model="state.month.cronEvery" label="3"
            >{{ state.text.Month.specific }}
              <el-select multiple v-model="state.month.specificSpecific">
                <el-option
                    v-for="(val, index) in 12"
                    :key="index"
                    :label="val"
                    :value="val"
                ></el-option>
              </el-select>
            </el-radio>
          </el-row>
          <el-row>
            <el-radio v-model="state.month.cronEvery" label="4"
            >{{ state.text.Month.cycle[0] }}
              <el-input-number
                  v-model="state.month.rangeStart"
                  :min="1"
                  :max="12"
              ></el-input-number>
              {{ state.text.Month.cycle[1] }}
              <el-input-number


                  v-model="state.month.rangeEnd"
                  :min="1"
                  :max="12"
              ></el-input-number>
            </el-radio>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>
    <div class="bottom">
      <div class="value">
        <span>
          cron预览:
        </span>
        <el-tag type="" size="large">
          {{ state.cron }}
        </el-tag>
      </div>
      <div class="buttonDiv">
        <el-button type="primary" @click.stop="handleChange">{{ state.text.Save }}</el-button>
        <el-button type="primary" @click="close">{{ state.text.Close }}</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import {reactive, computed, toRefs, defineComponent} from "vue";

export default defineComponent({
  name: "cronExpression",
  props: {
    cronValue: {},
    i18n: {},
    maxHeight: {}
  },
  setup(props, {emit}) {
    const {i18n} = toRefs(props)
    const state = reactive({
      second: {
        cronEvery: "1",
        incrementStart: 3,
        incrementIncrement: 5,
        rangeStart: 0,
        rangeEnd: 0,
        specificSpecific: [],
      },
      minute: {
        cronEvery: "1",
        incrementStart: 3,
        incrementIncrement: 5,
        rangeStart: 0,
        rangeEnd: 2,
        specificSpecific: [],
      },
      hour: {
        cronEvery: "1",
        incrementStart: 3,
        incrementIncrement: 5,
        rangeStart: 0,
        rangeEnd: 1,
        specificSpecific: [],
      },
      day: {
        cronEvery: "1",
        incrementStart: 1,
        incrementIncrement: 1,
        rangeStart: 0,
        rangeEnd: 0,
        specificSpecific: [],
        cronLastSpecificDomDay: 1,
        cronDaysBeforeEomMinus: 0,
        cronDaysNearestWeekday: 0,
      },
      week: {
        cronEvery: "1",
        incrementStart: 1,
        incrementIncrement: 1,
        specificSpecific: [],
        cronNthDayDay: 1,
        cronNthDayNth: 1,
      },
      month: {
        cronEvery: "1",
        incrementStart: 3,
        incrementIncrement: 5,
        rangeStart: 1,
        rangeEnd: 2,
        specificSpecific: [],
      },
      year: {
        cronEvery: "1",
        incrementStart: 2017,
        incrementIncrement: 1,
        rangeStart: 0,
        rangeEnd: 0,
        specificSpecific: [],
      },
      output: {
        // second: "",
        minute: "",
        hour: "",
        day: "",
        month: "",
        Week: "",
        // year: "",
      },
      text: {
        Seconds: {
          name: '秒',
          every: '每一秒钟',
          interval: ['每隔', '秒执行 从', '秒开始'],
          specific: '具体秒数(可多选)',
          cycle: ['周期从', '到', '秒']
        },
        Minutes: {
          name: '分',
          every: '每一分钟',
          interval: ['每隔', '分钟执行'],
          specific: '具体分钟数(可多选)',
          cycle: ['周期从', '到', '分']
        },
        Hours: {
          name: '时',
          every: '每一小时',
          interval: ['每隔', '小时执行'],
          specific: '具体小时数(可多选)',
          cycle: ['周期从', '到', '小时']
        },
        Day: {
          name: '天',
          every: '每一天',
          intervalWeek: ['每隔', '周执行'],
          intervalDay: ['每隔', '天执行'],
          specificWeek: '具体星期几(可多选)',
          specificDay: '具体天数(可多选)',
          lastDay: '在这个月的最后一天',
          lastWeekday: '在这个月的最后一个工作日',
          lastWeek: ['在这个月的最后一个'],
          beforeEndMonth: ['在本月底前', '天'],
          nearestWeekday: ['最近的工作日（周一至周五）至本月', '日'],
          someWeekday: ['在这个月的第', '个'],
        },
        Week: {
          name: '周',
          every: '每一周',
          week: ['天', '一', '二', '三', '四', '五', '六'].map(val => '星期' + val),
        },
        Month: {
          name: '月',
          every: '每一月',
          interval: ['每隔', '月执行',],
          specific: '具体月数(可多选)',
          cycle: ['从', '到', '月之间的每个月']
        },
        Year: {
          name: '年',
          every: '每一年',
          interval: ['每隔', '年执行 从', '年开始'],
          specific: '具体年份(可多选)',
          cycle: ['从', '到', '年之间的每一年']
        },
        Save: '保存',
        Close: '关闭'
      },
      secondsText: computed(() => {
        let seconds = "";
        let cronEvery = state.second.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            seconds = "*";
            break;
          case "2":
            seconds =
                state.second.incrementStart +
                "/" +
                state.second.incrementIncrement;
            break;
          case "3":
            state.second.specificSpecific.map((val) => {
              seconds += val + ",";
            });
            seconds = seconds.slice(0, -1);
            break;
          case "4":
            seconds = state.second.rangeStart + "-" + state.second.rangeEnd;
            break;
        }
        return seconds;
      }),
      minutesText: computed(() => {
        let minutes = "";
        let cronEvery = state.minute.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            minutes = "*";
            break;
          case "2":
            minutes =
                "*/" +
                state.minute.incrementIncrement;
            break;
          case "3":
            state.minute.specificSpecific.map((val) => {
              minutes += val + ",";
            });
            minutes = minutes.slice(0, -1);
            break;
          case "4":
            minutes = state.minute.rangeStart + "-" + state.minute.rangeEnd;
            break;
        }
        return minutes;
      }),
      hoursText: computed(() => {
        let hours = "";
        let cronEvery = state.hour.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            hours = "*";
            break;
          case "2":
            hours =
                "*/" + state.hour.incrementIncrement;
            break;
          case "3":
            state.hour.specificSpecific.map((val) => {
              hours += val + ",";
            });
            hours = hours.slice(0, -1);
            break;
          case "4":
            hours = state.hour.rangeStart + "-" + state.hour.rangeEnd;
            break;
        }
        return hours;
      }),
      daysText: computed(() => {
        let days = "";
        let cronEvery = state.day.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            break;
          case "2":
          case "4":
          case "11":
            days = "*";
            break;
          case "3":
            days =
                "*/" + state.day.incrementIncrement;
            break;
          case "5":
            state.day.specificSpecific.map((val) => {
              days += val + ",";
            });
            days = days.slice(0, -1);
            break;
          case "6":
            days = "L";
            break;
          case "7":
            days = "LW";
            break;
          case "8":
            days = state.day.cronLastSpecificDomDay + "L";
            break;
          case "9":
            days = "L-" + state.day.cronDaysBeforeEomMinus;
            break;
          case "10":
            days = state.day.cronDaysNearestWeekday + "W";
            break;
        }
        return days;
      }),
      weeksText: computed(() => {
        let weeks = "";
        let cronEvery = state.day.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
          case "3":
          case "5":
            weeks = "*";
            break;
          case "2":
            weeks =
                "*/" + state.week.incrementIncrement;
            break;
          case "4":
            state.week.specificSpecific.map((val) => {
              weeks += val + ",";
            });
            weeks = weeks.slice(0, -1);
            break;
          case "6":
          case "7":
          case "8":
          case "9":
          case "10":
            weeks = "*";
            break;
          case "11":
            weeks = state.week.cronNthDayDay + "#" + state.week.cronNthDayNth;
            break;
        }
        return weeks;
      }),
      monthsText: computed(() => {
        let months = "";
        let cronEvery = state.month.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            months = "*";
            break;
          case "2":
            months =
                "*/" + state.month.incrementIncrement;
            break;
          case "3":
            state.month.specificSpecific.map((val) => {
              months += val + ",";
            });
            months = months.slice(0, -1);
            break;
          case "4":
            months = state.month.rangeStart + "-" + state.month.rangeEnd;
            break;
        }
        return months;
      }),
      yearsText: computed(() => {
        let years = "";
        let cronEvery = state.year.cronEvery;
        switch (cronEvery.toString()) {
          case "1":
            years = "*";
            break;
          case "2":
            years =
                state.year.incrementStart + "/" + state.year.incrementIncrement;
            break;
          case "3":
            state.year.specificSpecific.map((val) => {
              years += val + ",";
            });
            years = years.slice(0, -1);
            break;
          case "4":
            years = state.year.rangeStart + "-" + state.year.rangeEnd;
            break;
        }
        return years;
      }),
      cron: computed(() => {
        return `${state.minutesText ||
        "*"} ${state.hoursText || "*"} ${state.daysText ||
        "*"} ${state.monthsText || "*"} ${state.weeksText ||
        "*"}`;
        // return `${state.secondsText || "*"} ${state.minutesText ||
        //   "*"} ${state.hoursText || "*"} ${state.daysText ||
        //   "*"} ${state.monthsText || "*"} ${state.weeksText ||
        //   "?"} ${state.yearsText || "*"}`;
      }),
    });
    const getValue = () => {
      return state.cron
    }
    const close = () => {
      emit('close')
    }
    const handleChange = () => {
      emit('change', state.cron)
      close()
    }
    const rest = (data) => {
      for (let i in data) {
        if (data[i] instanceof Object) {
          this.rest(data[i]);
        } else {
          switch (typeof data[i]) {
            case "object":
              data[i] = [];
              break;
            case "string":
              data[i] = "";
              break;
          }
        }
      }
    }
    return {
      state,
      getValue,
      close,
      handleChange,
      rest
    }
  },
});
</script>
<style lang="scss" scoped>
.vue3-cron-div {
  .el-input-number__decrease, .el-input-number__increase {
    top: 2px !important
  }

  .el-tabs {
    box-shadow: none;
  }

  .tabBody {
    overflow: auto;

    .el-row {
      margin: 20px 0;

      .long {
        .el-select {
          width: 350px;
        }
      }

      .el-input-number {
        width: 110px;
      }
    }
  }

  .myScroller {
    &::-webkit-scrollbar {
      /*滚动条整体样式*/
      width: 5px; /*高宽分别对应横竖滚动条的尺寸*/
      height: 1px;
    }

    &::-webkit-scrollbar-thumb {
      /*滚动条里面小方块*/
      border-radius: 10px;
      background-color: skyblue;
      background-image: -webkit-linear-gradient(
              45deg,
              rgba(255, 255, 255, 0.2) 25%,
              transparent 25%,
              transparent 50%,
              rgba(255, 255, 255, 0.2) 50%,
              rgba(255, 255, 255, 0.2) 75%,
              transparent 75%,
              transparent
      );
    }

    &::-webkit-scrollbar-track {
      /*滚动条里面轨道*/
      box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
      background: #ededed;
      border-radius: 10px;
    }
  }

  .bottom {
    width: 100%;
    margin-top: 5px;
    display: flex;
    align-items: center;
    justify-content: space-around;

    .value {
      float: left;
      font-size: 15px;
      vertical-align: middle;

      span:nth-child(1) {
        color: red
      }
    }
  }
}
</style>
