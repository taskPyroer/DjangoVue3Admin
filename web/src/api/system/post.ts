import request from '@/utils/request';

// 查询岗位列表
export function listPost(query:any) {
	return request({
		url: '/system/post/',
		method: 'get',
		params: query
	})
}

// 查询岗位详细
export function getPost(postId:number) {
	return request({
		url: '/system/post/' + postId + '/',
		method: 'get'
	})
}

// 获取角色表里所有的角色
export function getAllPosts() {
	return request({
		url: '/system/post/get-all-posts/',
		method: 'get'
	})
}

// 新增岗位
export function addPost(data:any) {
	return request({
		url: '/system/post/',
		method: 'post',
		data: data
	})
}

// 修改岗位
export function updatePost(data:any) {
	return request({
		url: '/system/post/' + data.id + '/',
		method: 'put',
		data: data
	})
}

// 删除岗位
export function delPost(postId: string) {
	return request({
		url: '/system/post/' + postId + '/',
		method: 'delete'
	})
}

// 导出
export function exportPost() {
	return request({
		url: '/system/post/export_to_excel/',
		method: 'get',
		responseType: 'blob'
	})
}
