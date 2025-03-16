"""
Time:     2023/8/22 10:40
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
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
            # 查询数据库或其他操作获取数据
            unique_api_groups = APIS.objects.order_by('api_group').values('api_group').distinct()
            # 将获取的数据缓存起来，并设置缓存过期时间为1天
            cache.set('api_group', unique_api_groups, 1 * 24 * 60 * 60)

        return DetailResponse(data={
            'api_groups': unique_api_groups,
        }, msg="获取成功")

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        # 获取当前对象
        from casbin_adapter.models import CasbinRule

        instance = self.get_object()
        old_v1 = instance.path  # 获取旧的值
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # 更新符合条件的数据
        updated_fields = {'v1': request.data['path'], 'v2': request.data['method']}

        CasbinRule.objects.filter(v1=old_v1).update(**updated_fields)

        self.perform_update(serializer)

        return DetailResponse(data=[], msg="更新成功")