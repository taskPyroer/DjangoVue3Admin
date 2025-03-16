"""
Time:     2023/12/3 14:13
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import re_path
from rest_framework import routers

from app_operation_log.views import OperationLogViewSet

system_url = routers.SimpleRouter()
system_url.register(r'operation-log', OperationLogViewSet)

urlpatterns = [
    re_path('operation-log/delete-all-logs/', OperationLogViewSet.as_view({'get': 'delete_all_logs'})),
    re_path('operation-log/get-read-logs/', OperationLogViewSet.as_view({'get': 'get_read_logs'}))
]
urlpatterns += system_url.urls