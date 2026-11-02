"""
Time:     2023/12/5 16:00
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:     routing.py
Describe: 存放websocket请求相关的路由信息
"""
from django.urls import path
from .websocketConfig import MegCenter

websocket_urlpatterns = [
    path('ws/<str:service_uid>/', MegCenter.as_asgi()),
]
