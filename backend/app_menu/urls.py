"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe: 
"""
from django.urls import re_path
from rest_framework import routers

from app_menu.views import MenuViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)

urlpatterns = [
    re_path('menu/menu-tree/', MenuViewSet.as_view({"get": "menu_tree"})),
    re_path('menu/menu-tree-simple/', MenuViewSet.as_view({"get": "menu_tree_simple"})),
]
urlpatterns += system_url.urls