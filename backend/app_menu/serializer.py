"""
Time:     2023/8/24 11:18
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
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
    菜单表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, instance):
        queryset = Menu.objects.filter(parent=instance.id).filter(status='0')
        if queryset:
            serializer = MenuTreeSerializer(queryset, many=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]