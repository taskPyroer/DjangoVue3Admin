"""
Time:     2023/8/6 16:07
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:
Describe: 自定义视图集
"""
from rest_framework.viewsets import ModelViewSet

# from utils.filters import DataLevelPermissionsFilter
from utils.json_response import SuccessResponse, ErrorResponse, DetailResponse
from utils.permission import CustomPermission
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import utils
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated


class CustomDjangoFilterBackend(DjangoFilterBackend):
    """
    自定义DjangoFilterBackend过滤，重新支持filter_fields，filter_class
    新版本：django-filter==22.1开始弃用21.1版本及以下的filter_fields，filter_class
    改为：filterset_fields和filterset_class
    """

    def get_filterset_class(self, view, queryset=None):
        """
        Return the `FilterSet` class used to filter the queryset.
        """
        filterset_class = getattr(view, 'filterset_class', None)
        filterset_fields = getattr(view, 'filterset_fields', None)

        if filterset_class is None and hasattr(view, 'filter_class'):
            utils.deprecate(
                "`%s.filter_class` attribute should be renamed `filterset_class`."
                % view.__class__.__name__)
            filterset_class = getattr(view, 'filter_class', None)

        if filterset_fields is None and hasattr(view, 'filter_fields'):
            utils.deprecate(
                "`%s.filter_fields` attribute should be renamed `filterset_fields`."
                % view.__class__.__name__)
            filterset_fields = getattr(view, 'filter_fields', None)

        if filterset_class:
            filterset_model = filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(queryset.model, filterset_model), \
                    'FilterSet model %s does not match queryset model %s' % \
                    (filterset_model, queryset.model)

            return filterset_class

        if filterset_fields and queryset is not None:
            MetaBase = getattr(self.filterset_base, 'Meta', object)

            class AutoFilterSet(self.filterset_base):
                class Meta(MetaBase):
                    model = queryset.model
                    fields = filterset_fields

            return AutoFilterSet

        return None


class CustomModelViewSet(ModelViewSet):
    """
    自定义的ModelViewSet:
    统一标准的返回格式;新增,查询,修改可使用不同序列化器
    (1)ORM性能优化, 尽可能使用values_queryset形式
    (2)create_serializer_class 新增时,使用的序列化器
    (3)update_serializer_class 修改时,使用的序列化器
    """
    values_queryset = None
    ordering_fields = '__all__'
    create_serializer_class = None
    update_serializer_class = None
    filterset_fields = ()
    # filterset_fields = '__all__'
    search_fields = ()
    # extra_filter_backends = [DataLevelPermissionsFilter]
    extra_filter_backends = []
    permission_classes = [IsAuthenticated, CustomPermission]  # IsAuthenticated:拒绝任何未经身份验证的用户的权限，而允许其他用户的权限
    filter_backends = [CustomDjangoFilterBackend, OrderingFilter, SearchFilter]

    def filter_queryset(self, queryset):
        for backend in set(set(self.filter_backends) | set(self.extra_filter_backends or [])):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        if getattr(self, 'values_queryset', None):
            return self.values_queryset
        return super().get_queryset()

    def get_serializer_class(self):
        action_serializer_name = f"{self.action}_serializer_class"
        action_serializer_class = getattr(self, action_serializer_name, None)
        if action_serializer_class:
            return action_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return DetailResponse(data=serializer.data, msg="更新成功")

    # 增强drf得批量删除功能 ：http请求方法：delete 如： url /api/admin/user/1,2,3/ 批量删除id 1，2，3得用户
    def get_object_list(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {f"{self.lookup_field}__in": self.kwargs[lookup_url_kwarg].split(',')}
        obj = queryset.filter(**filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    # 重写delete方法，让它支持批量删除 如：  /api/admin/user/1,2,3/ 批量删除id 1，2，3得用户
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object_list()
        self.perform_destroy(instance)
        return DetailResponse(data=[], msg="删除成功")

    def perform_destroy(self, instance):
        instance.delete()