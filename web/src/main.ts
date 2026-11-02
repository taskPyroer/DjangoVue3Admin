import {createApp} from 'vue';
import App from './App.vue';
import pinia from '@/stores/index';
import router from './router';
import {directive} from '@/utils/directive';
import {i18n} from '@/i18n/index';
import other from '@/utils/other';
import {selectDictLabel, download} from '@/utils';
import {getDicts} from "@/api/system/dict/data";
import {dateStrFormat} from "@/utils/formatTime";
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import '@/theme/index.scss';
import mitt from 'mitt';
import WebSocketService from '@/api/WebSocketService';

const app = createApp(App);

directive(app);
other.elSvg(app);

app
    .use(ElementPlus)
    .use(i18n)
    .use(pinia)
    .use(router)
    .mount('#app');

// 全局方法挂载
app.config.globalProperties.getDicts = getDicts;
app.config.globalProperties.mittBus = mitt();
app.config.globalProperties.selectDictLabel = selectDictLabel;
app.config.globalProperties.download = download;
app.config.globalProperties.dateStrFormat = dateStrFormat;
// 注册WebSocket服务
app.config.globalProperties.$websocket = WebSocketService;
