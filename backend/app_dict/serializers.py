"""
Time:     2023/9/11 14:51
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe:
"""
from rest_framework import serializers

from app_dict.models import DictData, DictType
from utils.serializers import CustomModelSerializer
from utils.validator import CustomUniqueValidator


class DictTypeSerializer(CustomModelSerializer):
    """
   字典类型-序列化器
    """
    class Meta:
        model = DictType
        fields = "__all__"
        read_only_fields = ["id"]


class DictTypeCreateSerializer(CustomModelSerializer):
    """
    字典类型修改/更新-序列化器
    """
    dict_name = serializers.CharField(
        max_length=64,
        validators=[CustomUniqueValidator(queryset=DictType.objects.all(), message="字典名称必须唯一")])
    dict_type = serializers.CharField(
        max_length=64,
        validators=[CustomUniqueValidator(queryset=DictType.objects.all(), message="字典类型必须唯一")])

    class Meta:
        model = DictType
        fields = "__all__"
        read_only_fields = ["id"]


class DictDataSerializer(CustomModelSerializer):
    """
   字典数值-序列化器
    """
    class Meta:
        model = DictData
        fields = "__all__"
        read_only_fields = ["id"]
