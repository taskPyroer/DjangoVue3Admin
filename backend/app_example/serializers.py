"""  
Time:     2025/06/23 10:00
Author:   Django Vue3 Admin Example
Version:  V 0.1
File:     serializers
Describe: 示例模块序列化器 - 基础增删改查
"""
from app_example.models import Example
from utils.serializers import CustomModelSerializer


class ExampleSerializer(CustomModelSerializer):
    """
    示例-序列化器
    """
    class Meta:
        model = Example
        fields = "__all__"


class ExampleCreateUpdateSerializer(CustomModelSerializer):
    """
    示例管理 创建/更新时的序列化器
    """
    class Meta:
        model = Example
        fields = "__all__"
        read_only_fields = ['id']  # 将id字段设置为只读，这样在创建时不需要提供