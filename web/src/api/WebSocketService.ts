import { ElNotification } from 'element-plus';
import { Session } from "@/utils/storage";

let socket: WebSocket | null = null;

export function initWebSocket() {
    const rawToken = Session.get('token');
    const token = rawToken ? String(rawToken).replace("JWT ", "") : "";
    if (token) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            return;
        }
        const apiBase = import.meta.env.VITE_API_URL || window.location.origin;
        const isHttps = apiBase.startsWith('https://') || window.location.protocol === 'https:';
        const host = apiBase.replace(/^https?:\/\//, '');
        const wsProtocol = isHttps ? 'wss://' : 'ws://';
        const webUrl = `${wsProtocol}${host}/ws/${token}/`;

        try {
            socket = new WebSocket(webUrl);
            socket.onerror = webSocketOnError;
            socket.onmessage = webSocketOnMessage;
            socket.onclose = () => {
                socket = null;
            };
        } catch (e) {
            console.error('WebSocket 初始化失败:', e);
        }
    }
}

export function webSocketOnError(e: any) {
    console.error('WebSocket连接错误:', e);
}

/**
 * 接收消息
 */
export function webSocketOnMessage(e: any) {
    try {
        const data = typeof e.data === 'string' ? JSON.parse(e.data) : e.data;
        if (!data) return;

        const typeMap: Record<string, 'success' | 'error' | 'info' | 'warning'> = {
            SYSTEM: 'success',
            ERROR: 'error',
            INFO: 'info',
            WARNING: 'warning',
        };

        const noticeType = typeMap[data.contentType] || 'info';
        const titleMap: Record<string, string> = {
            SYSTEM: '系统消息',
            ERROR: '系统错误',
            INFO: '温馨提示',
            WARNING: '告警提示',
        };

        ElNotification({
            title: titleMap[data.contentType] || '消息通知',
            message: data.content || '',
            type: noticeType,
            position: 'bottom-right',
            duration: noticeType === 'error' ? 5000 : 3000,
        });
    } catch (err) {
        console.warn('WebSocket 消息解析非标准格式:', e.data);
    }
}

// 关闭Websocket
export function closeWebsocket() {
    if (socket) {
        socket.close();
        socket = null;
    }
}

/**
 * 发送消息
 */
export function webSocketSend(message: any) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(typeof message === 'string' ? message : JSON.stringify(message));
    }
}

export default {
    initWebSocket,
    closeWebsocket,
    webSocketSend,
};
