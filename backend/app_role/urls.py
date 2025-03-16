"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import re_path
from rest_framework import routers

from app_role.views import RoleViewSet

system_url = routers.SimpleRouter()
system_url.register(r'role', RoleViewSet)

urlpatterns = [
    re_path('role/role-id-to-menu/(?P<pk>.*?)/', RoleViewSet.as_view({'get': 'get_policy_path_role'})),
    re_path('role/get-all-roles/', RoleViewSet.as_view({'get': 'get_all_roles'})),
]
urlpatterns += system_url.urls