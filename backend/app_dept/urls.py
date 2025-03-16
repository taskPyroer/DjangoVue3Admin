"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe:
"""
from django.urls import re_path
from rest_framework import routers

from app_dept.views import DeptViewSet

system_url = routers.SimpleRouter()
system_url.register(r'dept', DeptViewSet)

urlpatterns = [
    re_path('dept/dept-tree/', DeptViewSet.as_view({"get": "dept_tree"}))
]
urlpatterns += system_url.urls