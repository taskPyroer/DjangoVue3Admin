import request from '@/utils/request';

// 查询公告列表
export function listSendNotice(query:any) {
    return request({
        url: '/system/message-center/',
        method: 'get',
        params: query
    })
}

// 查询公告详细
export function getNotice(id:any) {
    return request({
        url: '/system/message-center/' + id + '/',
        method: 'get',
    })
}

// 查询我接收的列表
export function listReceiveNotice(query:any) {
    return request({
        url: '/system/message-center/get-self-receive/',
        method: 'get',
        params: query
    })
}

// 新增公告
export function addNotice(data:any) {
    return request({
        url: '/system/message-center/',
        method: 'post',
        data: data
    })
}

// 删除公告
export function delNotice(noticeId: string) {
    return request({
        url: '/system/message-center/' + noticeId + '/',
        method: 'delete'
    })
}
