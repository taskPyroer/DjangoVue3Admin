import request from '@/utils/request';


// 查询菜单下拉树结构
export function treeselect() {
	return request({
		url: '/system/menu/menu-tree/',
		method: 'get'
	})
}

// 查询菜单下拉树结构
export function treeselectSimple() {
	return request({
		url: '/system/menu/menu-tree-simple/',
		method: 'get'
	})
}


// 查询菜单列表
export function listMenu(query: Array<object>) {
	return request({
		url: '/system/menu/',
		method: 'get',
		params: query
	})
}


// 新增菜单
export function addMenu(data: any) {
	return request({
		url: '/system/menu/',
		method: 'post',
		data: data
	})
}

// 修改菜单
export function updateMenu(data: any) {
	return request({
		url: '/system/menu/' + data.id + '/',
		method: 'put',
		data: data
	})
}

// 删除菜单
export function delMenu(menuId: number) {
	return request({
		url: '/system/menu/' + menuId + '/',
		method: 'delete'
	})
}
