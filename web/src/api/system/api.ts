import request from '@/utils/request';

// 查询参数列表分页
export function listApi(query: any) {
    return request({
        url: '/system/apis/',
        method: 'get',
        params: query
    })
}

// 查询参数列表
export function listApiAll(query: any) {
    return request({
        url: '/system/apis/?page=1&pageSize=999&enable_datasource=0',
        method: 'get',
        params: query
    })
}

// 查询参数详细
export function getApi(id: any) {
    return request({
        url: '/system/apis/' + id + '/',
        method: 'get'
    })
}

// 新增参数配置
export function addApi(data: any) {
    return request({
        url: '/system/apis/',
        method: 'post',
        data: data
    })
}

// 修改参数配置
export function updateApi(data: any) {
    return request({
        url: '/system/apis/' + data.id + '/',
        method: 'put',
        data: data
    })
}

// 删除参数配置
export function delApi(id: any) {
    return request({
        url: '/system/apis/' + id + '/',
        method: 'delete'
    })
}

// 获取权限Api通过角色id
export function getPolicyPathByRoleId(id: any) {
    return request({
        url: '/system/role/role-id-to-menu/' + id + '/',
        method: 'get'
    })
}

// 获取所有的API组
export function getApiGroup() {
    return request({
        url: '/system/apis/get-all-api-group/',
        method: 'get',
    })
}
