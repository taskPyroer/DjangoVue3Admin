"""
Time:     2023/8/6 16:07
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:
Describe: 自定义序列化器
"""
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from app_user.models import Users


class CustomModelSerializer(ModelSerializer):
    """
    增强DRF的ModelSerializer,可自动更新模型的审计字段记录
    (1)self.request能获取到rest_framework.request.Request对象
    """
    # 修改人的审计字段名称, 默认modifier, 继承使用时可自定义覆盖
    modifier_field_id = 'modifier'
    modifier_name = serializers.SerializerMethodField(read_only=True)

    def get_modifier_name(self, instance):
        if not hasattr(instance, 'modifier'):
            return None
        modifier_id = getattr(instance, 'modifier', None)
        if not modifier_id:
            return None
        # 使用 context 级局部缓存，彻底消除列表序列化时的 N+1 重复查库
        cache = self.context.setdefault('_user_nickname_cache', {})
        if modifier_id in cache:
            return cache[modifier_id]
        name = Users.objects.filter(id=modifier_id).values_list('nickname', flat=True).first()
        cache[modifier_id] = name
        return name

    # 创建人的审计字段名称, 默认creator, 继承使用时可自定义覆盖
    creator_field_id = 'creator'
    creator_name = serializers.SlugRelatedField(slug_field="nickname", source="creator", read_only=True)
    # 添加默认时间返回格式
    create_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_datetime = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    def __init__(self, instance=None, data=empty, request=None, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.request: Request = request or self.context.get('request', None)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        if self.request and getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            if self.modifier_field_id in self.fields.fields:
                validated_data[self.modifier_field_id] = self.get_request_user_id()
            if self.creator_field_id in self.fields.fields:
                validated_data[self.creator_field_id] = self.request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if self.request and getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            if self.modifier_field_id in self.fields.fields:
                validated_data[self.modifier_field_id] = self.get_request_user_id()
            if hasattr(self.instance, self.modifier_field_id):
                setattr(self.instance, self.modifier_field_id, self.get_request_user_id())
        return super().update(instance, validated_data)

    def get_request_username(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'username', None)
        return None

    def get_request_nickname(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'nickname', None)
        return None

    def get_request_user_id(self):
        if getattr(self.request, 'user', None):
            return getattr(self.request.user, 'id', None)
        return None
