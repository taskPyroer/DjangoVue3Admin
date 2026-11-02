"""
Time:     2023/8/23 15:51
Author:   公众号【布鲁的Python之旅】
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
        # 转换为拼音首字母作为基础key
        pinyin_list = pinyin(dept_name, style=Style.FIRST_LETTER)
        base_key = ''.join([x[0] for x in pinyin_list]) or 'dept'
        dept_key = base_key
        
        # 排除当前正在编辑的实例
        current_id = getattr(self.instance, 'id', None) if hasattr(self, 'instance') else None
        
        suffix = 1
        while True:
            qs = Dept.objects.filter(dept_key=dept_key)
            if current_id:
                qs = qs.exclude(id=current_id)
            if qs.exists():
                suffix += 1
                dept_key = f"{base_key}{suffix}"
            else:
                break
        validated_data['dept_key'] = dept_key
        return validated_data

    def create(self, validated_data):
        if 'dept_name' in validated_data:
            validated_data = self.rename(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 仅当dept_name被实际修改时才重新生成dept_key
        if 'dept_name' in validated_data and validated_data['dept_name'] != instance.dept_name:
            validated_data = self.rename(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id", "dept_key"]


class DeptTreeSerializer(CustomModelSerializer):
    """
    部门表的树形序列化器（兼容类声明）
    """
    class Meta:
        model = Dept
        fields = "__all__"
        read_only_fields = ["id"]