"""
Time:     2023/11/21 14:31
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     celery_clocked_schedule.py
Describe: 指定某个时间执行定时任务的控制器 (例：每年的12月星期一的8:30)
"""
from django_celery_beat.models import ClockedSchedule

from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class ClockedScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = ClockedSchedule
        read_only_fields = ["id"]
        fields = '__all__'


class ClockedScheduleModelViewSet(CustomModelViewSet):
    """
    时钟时间（DateTimeField）运行一次性任务
    """
    queryset = ClockedSchedule.objects.all()
    serializer_class = ClockedScheduleSerializer
