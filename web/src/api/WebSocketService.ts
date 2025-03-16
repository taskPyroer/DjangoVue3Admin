import {ElNotification} from 'element-plus';
import {Session} from "@/utils/storage"

let socket: WebSocket | null = null;

export function initWebSocket() {
    const token = Session.get('token').replace("JWT ", ""); // 获取浏览器缓存 token 值
    if (token) {
        const webUrl = `ws://${import.meta.env.VITE_API_URL.replace('http://', '')}/ws/${token}/`;
        socket = new WebSocket(webUrl);
        socket.onerror = webSocketOnError;
        socket.onmessage = webSocketOnMessage;
        socket.onclose = closeWebsocket;
    }
}

export function webSocketOnError(e: any) {
    ElNotification({
        title: '',
        message: 'WebSocket连接发生错误' + JSON.stringify(e),
        type: 'error',
        position: 'bottom-right',
        duration: 3000
    });
}

/**
 * 接收消息
 * @param e
 * @returns {any}
 */
export function webSocketOnMessage(e: any) {
    const data = JSON.parse(e.data);
    if (data.contentType === 'SYSTEM') {
        ElNotification({
            title: '系统消息',
            message: data.content,
            type: 'success',
            position: 'bottom-right',
            duration: 3000
        });
    } else if (data.contentType === 'ERROR') {
        ElNotification({
            title: '',
            message: data.content,
            type: 'error',
            position: 'bottom-right',
            duration: 0
        });
    } else if (data.contentType === 'INFO') {
        ElNotification({
            title: '温馨提示',
            message: data.content,
            type: 'success',
            position: 'bottom-right',
            duration: 0
        });
    } else {
        ElNotification({
            title: '温馨提示',
            message: data.content,
            type: 'info',
            position: 'bottom-right',
            duration: 3000
        });
    }
}

// 关闭Websocket
export function closeWebsocket() {
    ElNotification({
        title: 'websocket',
        message: '连接已关闭...',
        type: 'error',
        position: 'bottom-right',
        duration: 3000
    });
}

/**
 * 发送消息
 * @param message
 * @param socket
 */
export function webSocketSend(message: any, socket: WebSocket) {
    socket.send(JSON.stringify(message));
}

export default {
    initWebSocket, closeWebsocket, webSocketSend
}
