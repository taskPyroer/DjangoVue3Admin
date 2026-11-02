"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:     urls
Describe:
"""
# Create your views here.
from django.core.cache import cache
from django.db import transaction

from app_apis.models import APIS
from app_apis.serializers import ApiSerializer
from utils.json_response import DetailResponse
from utils.viewset import CustomModelViewSet


class ApisViewSet(CustomModelViewSet):
    queryset = APIS.objects.all()
    serializer_class = ApiSerializer
    filterset_fields = ['api_group', 'method', 'enable_datasource']
    search_fields = ['path', 'description']

    def get_all_api_group(self, request, *args, **kwargs):
        """
        获取API所有的分组
        """
        unique_api_groups = cache.get('api_group')
        if unique_api_groups is None:
            unique_api_groups = list(APIS.objects.order_by('api_group').values('api_group').distinct())
            cache.set('api_group', unique_api_groups, 1 * 24 * 60 * 60)

        return DetailResponse(data={
            'api_groups': unique_api_groups,
        }, msg="获取成功")

    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete('api_group')

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete('api_group')

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        from casbin_adapter.models import CasbinRule

        instance = self.get_object()
        old_v1 = instance.path  # 获取旧的路径
        old_v2 = instance.method
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        serializer.is_valid(raise_exception=True)

        new_path = serializer.validated_data.get('path', old_v1)
        new_method = serializer.validated_data.get('method', old_v2)

        # 同步更新 Casbin 策略中的路由与请求方式
        CasbinRule.objects.filter(v1=old_v1, v2=old_v2).update(v1=new_path, v2=new_method)

        self.perform_update(serializer)
        cache.delete('api_group')

        return DetailResponse(data=serializer.data, msg="更新成功")