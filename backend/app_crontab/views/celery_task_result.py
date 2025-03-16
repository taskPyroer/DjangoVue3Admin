"""
Time:     2023/11/21 14:58
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     celery_task_result
Describe: 
"""
from django_celery_results.models import TaskResult

from app_crontab.filters import CeleryTaskResultFilterSet
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class CeleryTaskResultSerializer(CustomModelSerializer):
    """
    定时任务结果 序列化器
    """

    class Meta:
        model = TaskResult
        fields = '__all__'


class CeleryTaskResultViewSet(CustomModelViewSet):
    """
    定时任务结果 接口
    """
    queryset = TaskResult.objects.all()
    serializer_class = CeleryTaskResultSerializer
    filter_class = CeleryTaskResultFilterSet
