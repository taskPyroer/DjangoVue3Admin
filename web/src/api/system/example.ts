import request from '@/utils/request';

// 查询示例列表
export function listExample(query : any) {
	return request({
		url: '/system/example/',
		method: 'get',
		params: query
	})
}

// 查询示例详细
export function getExample(exampleId: number) {
	return request({
		url: '/system/example/' + exampleId + '/',
		method: 'get'
	})
}

// 新增示例
export function addExample(data:any) {
	return request({
		url: '/system/example/',
		method: 'post',
		data: data
	})
}

// 修改示例
export function updateExample(data:any) {
	return request({
		url: '/system/example/' + data.id + '/',
		method: 'put',
		data: data
	})
}

// 删除示例
export function delExample(exampleId: number) {
	return request({
		url: '/system/example/' + exampleId + '/',
		method: 'delete'
	})
}