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
                # 查询数据库获取白名单path列表
                api_white_list = list(APIS.objects.filter(enable_datasource='1').values_list('path', flat=True))
                # 将获取的数据缓存起来，并设置缓存过期时间为5天
                cache.set('api_white_list', api_white_list, 5 * 24 * 60 * 60)

            if action in api_white_list:
                return True
            method = request.method  # 当前请求方法
            role_keys = list(request.user.role.values_list('role_key', flat=True))
            if role_keys:
                # 构建批量查询请求，使用 batch_enforce 一次性检查权限，避免循环和重复查询
                batch_request = [(rk, action, method) for rk in role_keys]
                allowed = enforcer.batch_enforce(batch_request)
                return any(allowed)
            return False
