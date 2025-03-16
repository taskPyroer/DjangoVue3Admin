"""
Time:     2023/12/1 9:45
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import path
from rest_framework import routers

from app_monitor.views import MonitorManageViewSet

system_url = routers.SimpleRouter()
system_url.register(r'monitor', MonitorManageViewSet)

urlpatterns = [
    path('monitor/get-system-info/', MonitorManageViewSet.as_view({'get': 'get_system_info'}), name='实时获取本机监控信息'),

]
urlpatterns += system_url.urls
