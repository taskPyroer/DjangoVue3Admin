"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import path
from rest_framework import routers

from app_user.views import UserViewSet

system_url = routers.SimpleRouter()
system_url.register(r'user', UserViewSet)

urlpatterns = [
    path('user/user-info/',UserViewSet.as_view({'get':'user_info'})),
    path('user/update-user-info/',UserViewSet.as_view({'put':'update_user_info'})),
    path('user/auth/',UserViewSet.as_view({'get':'auth'})),
    path('user/export_to_excel/', UserViewSet.as_view({'get': 'export_to_excel'}))
]
urlpatterns += system_url.urls