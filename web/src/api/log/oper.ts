import request from '@/utils/request';

// 查询参数列表分页
export function listOperInfo(query:any) {
    return request({
        url: '/system/operation-log/',
        method: 'get',
        params: query
    })
}

// 删除
export function delOperInfo(operId:any) {
    return request({
        url: '/system/operation-log/'+ operId + '/',
        method: 'delete',
    })
}

// 清空
export function cleanOpernfo() {
    return request({
        url: '/system/operation-log/delete-all-logs/',
        method: 'get',
    })
}

// 查询系统日志
export function SystemReadLogs(query:any) {
    return request({
        url: '/system/operation-log/get-read-logs/',
        method: 'get',
        params: query
    })
}
