import request from '@/utils/request'

// 查询定时任务调度列表
export function listJob(query:any) {
	return request({
		url: '/job/crontab/periodic-task/',
		method: 'get',
		params: query
	})
}

// 查询定时任务调度详细
export function listTaskResult(jobName:any) {
	return request({
		url: '/job/crontab/task-result/',
		method: 'get',
		params: jobName
	})
}

// 新增定时任务调度
export function addJob(data:any) {
	return request({
		url: '/job/crontab/periodic-task/',
		method: 'post',
		data: data
	})
}

// 修改定时任务调度
export function updateJob(data:any) {
	return request({
		url: '/job/crontab/periodic-task/' + data.id + '/',
		method: 'put',
		data: data
	})
}

// 删除定时任务调度
export function delJob(jobId:any) {
	return request({
		url: '/job/crontab/periodic-task/' + jobId + '/',
		method: 'delete'
	})
}

// 启动执行
export function runStopJob(jobId:any, enabled:boolean) {
	return request({
		url: '/job/crontab/periodic-task/enabled/'+ jobId + '/',
		method: 'put',
		data: {
			'enabled': enabled
		}
	})
}

// 获取本地所有的内置定时任务
export function listTask() {
	return request({
		url: '/job/crontab/periodic-task/tasklist/',
		method: 'get',
	})
}
