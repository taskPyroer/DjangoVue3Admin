from django.core.cache import cache
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from casbin_adapter.enforcer import enforcer

from utils.common import re_api


class CustomPermission(BasePermission):
    """自定义权限"""

    def has_permission(self, request, view):
        if isinstance(request.user, AnonymousUser):
            return False
        # 判断是否是超级管理员
        if request.user.is_superuser:
            return True
        else:
            api = request.path  # 当前请求接口
            action = re_api(api)
            api_white_list = cache.get('api_white_list')
            if api_white_list is None:
                from app_apis.models import APIS
                # 查询数据库或其他操作获取数据
                api_white_list = APIS.objects.filter(enable_datasource='1').values('path')
                # 将获取的数据缓存起来，并设置缓存过期时间为5天
                cache.set('api_white_list', api_white_list, 5 * 24 * 60 * 60)

            if action in api_white_list:
                return True
            method = request.method  # 当前请求方法
            role_keys = request.user.role.values_list('role_key')
            if role_keys.exists():
                # 构建一个批量查询的请求 使用 batch_enforce 检查权限
                batch_request = [(role_key[0], action, method) for role_key in role_keys]
                # 使用 batch_enforce 方法批量检查权限
                allowed = enforcer.batch_enforce(batch_request)
                if any(allowed):
                    return True
                else:
                    return False
            else:
                return False
