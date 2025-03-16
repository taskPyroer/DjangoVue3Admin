"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import path
from rest_framework import routers

from app_post.views import PostViewSet

system_url = routers.SimpleRouter()
system_url.register(r'post', PostViewSet)

urlpatterns = [
    path('post/get-all-posts/', PostViewSet.as_view({'get': 'get_all_posts'})),
    path('post/export_to_excel/', PostViewSet.as_view({'get': 'export_to_excel'}))
]
urlpatterns += system_url.urls