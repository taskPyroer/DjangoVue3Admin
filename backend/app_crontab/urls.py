"""
Time:     2023/11/21 10:31
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe:
"""

from django.urls import path, re_path
from rest_framework import routers

from app_crontab.views.celery_clocked_schedule import ClockedScheduleModelViewSet
from app_crontab.views.celery_interval_schedule import IntervalScheduleModelViewSet
from app_crontab.views.celery_crontab_schedule import CrontabScheduleModelViewSet
from app_crontab.views.celery_periodic_task import PeriodicTaskModelViewSet
from app_crontab.views.celery_task_result import CeleryTaskResultViewSet

system_url = routers.SimpleRouter()

system_url.register(r'interval-schedule', IntervalScheduleModelViewSet)
system_url.register(r'crontab-schedule', CrontabScheduleModelViewSet)
system_url.register(r'clocked-schedule', ClockedScheduleModelViewSet)
system_url.register(r'task-result', CeleryTaskResultViewSet)
system_url.register(r'periodic-task', PeriodicTaskModelViewSet)

urlpatterns = [
    re_path('periodic-task/enabled/(?P<pk>.*?)/', PeriodicTaskModelViewSet.as_view({'put': 'taskenabled'}), name='开始/暂停任务'),
    path('periodic-task/tasklist/', PeriodicTaskModelViewSet.as_view({'get': 'tasklist'}), name='获取本地所有tasks文件中的task任务方法'),
]

urlpatterns += system_url.urls