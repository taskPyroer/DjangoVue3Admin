"""
Time:     2023/12/6 16:44
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import re_path
from rest_framework import routers

from app_message.views import MessageCenterViewSet

system_url = routers.SimpleRouter()
system_url.register(r'message-center', MessageCenterViewSet)

urlpatterns = [
    re_path('message-center/get-unread-msg/', MessageCenterViewSet.as_view({"get": "get_unread_msg"})),
    re_path('message-center/get-newest-msg/', MessageCenterViewSet.as_view({"get": "get_newest_msg"})),
    re_path('message-center/get-self-receive/', MessageCenterViewSet.as_view({"get": "get_self_receive"})),
]
urlpatterns += system_url.urls