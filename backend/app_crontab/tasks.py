"""
Time:     2023/11/21 15:37
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     tasks
Describe:
"""
from application.celery import app
from celery import shared_task


@app.task(bind=True)
def cron_job_test(self):
    print(self.request)
    return "cron_job_test running"


@shared_task
def cron_job_add(x, y):
    print("cron_job_add running")
    return f"cron_job_add running: {x + y}"


@shared_task
def cron_job_mul(x, y):
    print("cron_job_mul running")
    return f"cron_job_mul running: {x * y}"
