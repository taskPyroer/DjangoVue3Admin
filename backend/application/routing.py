"""
Time:     2023/12/5 16:00
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     routing.py
Describe: 存放websocket请求相关的路由信息
"""
from django.urls import re_path, path
from .consumers import ChatConsumer
from .websocketConfig import MegCenter

websocket_urlpatterns = [
    # re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    path('ws/<str:service_uid>/', MegCenter.as_asgi()), #consumers.DvadminWebSocket 是该路由的消费者
]
