"""
Time:     2023/8/23 15:51
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe:
"""
from rest_framework import serializers

from app_dept.models import Dept
from utils.serializers import CustomModelSerializer
from utils.validator import CustomUniqueValidator


class DeptSerializer(CustomModelSerializer):
    """
    部门-序列化器
    """
    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id", "dept_key"]


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """
    dept_name = serializers.CharField(
        max_length=50,
        validators=[CustomUniqueValidator(queryset=Dept.objects.all(), message="部门必须唯一")])

    def rename(self, validated_data):
        from pypinyin import pinyin, Style
        dept_name = validated_data['dept_name']
        # 转换为拼音首字母
        pinyin_list = pinyin(dept_name, style=Style.FIRST_LETTER)
        dept_key = ''.join([x[0] for x in pinyin_list])
        # 追加递增的数字来确保唯一性
        suffix = 1
        while True:
            result = ''
            if Dept.objects.filter(dept_key=dept_key).exists():
                suffix += 1
                # 将转换后的拼音添加到结果字符串
                result += dept_key + str(suffix)
                dept_key = result
            else:
                break
        validated_data['dept_key'] = dept_key
        return validated_data

    def create(self, validated_data):
        if 'dept_name' in validated_data.keys():
            validated_data = self.rename(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'dept_name' in validated_data.keys():
            validated_data = self.rename(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id", "dept_key"]


class DeptTreeSerializer(CustomModelSerializer):
    """
    部门表的树形序列化器
    """
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, instance):
        queryset = Dept.objects.filter(parent=instance.id).exclude(status='1')
        if queryset:
            serializer = DeptTreeSerializer(queryset, many=True)
            return serializer.data
        else:
            return None

    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]