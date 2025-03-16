"""
Time:     2023/9/11 15:00
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe:
"""
from django.db import transaction

# Create your views here.
from app_dict.models import DictType, DictData
from app_dict.serializers import DictTypeSerializer, DictDataSerializer, DictTypeCreateSerializer
from utils.json_response import DetailResponse, ErrorResponse
from utils.viewset import CustomModelViewSet


class DictTypeViewSet(CustomModelViewSet):
    """
    系统-字典类型
    """
    queryset = DictType.objects.all()
    serializer_class = DictTypeSerializer
    create_serializer_class = DictTypeCreateSerializer
    update_serializer_class = DictTypeCreateSerializer
    filterset_fields = ['status']
    search_fields = ['dict_name', 'dict_type']

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        # 重写删除
        instances = self.get_object_list()
        try:
            with transaction.atomic():
                # 需要删除系统-字典数值的数据
                for instance in instances:
                    dict_data_instances = DictData.objects.filter(dict_type=instance.dict_type)
                    dict_data_instances.delete()

                self.perform_destroy(instances)
                return DetailResponse(data=[], msg="删除成功")
        except Exception as e:
            return ErrorResponse(data=[], msg="删除失败: {}".format(str(e)))

class DictDataViewSet(CustomModelViewSet):
    """
    系统-字典数值
    """
    queryset = DictData.objects.all()
    serializer_class = DictDataSerializer
    filterset_fields = ['dict_type', 'status']
    search_fields = ['dict_label']