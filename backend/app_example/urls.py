"""  
Time:     2025/06/23 10:00
Author:   Django Vue3 Admin Example
Version:  V 0.1
File:     urls
Describe: 示例模块URL配置 - 基础增删改查
"""
from rest_framework import routers

from app_example.views import ExampleViewSet

system_url = routers.SimpleRouter()
system_url.register(r'example', ExampleViewSet)

urlpatterns = system_url.urls