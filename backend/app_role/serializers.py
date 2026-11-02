"""
Time:     2023/8/28 14:19
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:     serializers
Describe: 
"""
from rest_framework import serializers
from casbin_adapter.enforcer import enforcer

from app_dept.models import Dept
from app_menu.models import Menu
from app_role.models import Role
from utils.serializers import CustomModelSerializer


class RoleSerializer(CustomModelSerializer):
    """
    角色-序列化器
    """
    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]


class RoleCreateSerializer(CustomModelSerializer):
    api = serializers.ListField(
        write_only=True,
        allow_null=True,  # 允许字段为空
        required=False  # 不强制要求字段存在
    )
    dept = serializers.PrimaryKeyRelatedField(
        queryset=Dept.objects.all(),
        many=True,
        allow_null=True,  # 允许字段为空
        required=False  # 不强制要求字段存在
    )
    menu = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(),
        many=True,
        allow_null=True,  # 允许字段为空
        required=False  # 不强制要求字段存在
    )

    def create(self, validated_data):
        if 'api' in validated_data.keys():
            api_data = validated_data.pop('api')
            # 在此处根据需要对 api 进行二次处理
            sub = validated_data['role_key']
            for item in api_data:
                enforcer.add_policy([sub, item['path'], item['method']])

        # 全局更新
        # set_data1 = list([sub, item['path'], item['method']] for item in api_data)
        # enforcer.add_policies(set_data1)
        # enforcer.save_policy()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        old_role_key = instance.role_key
        new_role_key = validated_data.get('role_key', old_role_key)

        if 'api' in validated_data:
            api_data = validated_data.pop('api')
            if old_role_key != new_role_key:
                enforcer.remove_filtered_policy(0, old_role_key)
                filtered_policy = []
            else:
                filtered_policy = enforcer.get_filtered_policy(0, new_role_key)

            set_data1 = set((new_role_key, item['path'], item['method']) for item in api_data)
            set_data2 = set(tuple(item) for item in filtered_policy)

            # 找出在data1中存在但在data2中不存在的元素，执行添加
            for element in (set_data1 - set_data2):
                enforcer.add_policy(*element)

            # 找出在data2中存在但在data1中不存在的元素,执行删除
            for element in (set_data2 - set_data1):
                enforcer.remove_policy(*element)
        elif old_role_key != new_role_key:
            # 仅修改了 role_key，同步迁移权限策略
            filtered_policy = enforcer.get_filtered_policy(0, old_role_key)
            for item in filtered_policy:
                enforcer.remove_policy(*item)
                enforcer.add_policy(new_role_key, item[1], item[2])

        return super().update(instance, validated_data)

    class Meta:
        model = Role
        fields = "__all__"
        read_only_fields = ["id"]
