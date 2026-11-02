"""
Time:     2023/8/24 11:18
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:     serializer
Describe: 
"""
from rest_framework import serializers

from app_menu.models import Menu
from utils.serializers import CustomModelSerializer


class MenuSerializer(CustomModelSerializer):

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class MenuTreeSerializer(CustomModelSerializer):
    """
    菜单表的树形序列化器（兼容类声明）
    """
    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]