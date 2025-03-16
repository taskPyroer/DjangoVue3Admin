"""
Time:     2023/11/21 10:27
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     celery_interval_schedule
Describe: 按时间间隔频率执行定时任务的控制器，(例：每间隔1H/1M/…执行一次)
"""
from django_celery_beat.models import IntervalSchedule

from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class IntervalScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = IntervalSchedule
        read_only_fields = ["id"]
        fields = '__all__'


class IntervalScheduleModelViewSet(CustomModelViewSet):
    """
    以特定（固定间隔）时间间隔（例如每 5 秒）运行的计划(每 /月/日/时/分/秒/微秒)
    DAYS = 'days'
    HOURS = 'hours'
    MINUTES = 'minutes'
    SECONDS = 'seconds'
    MICROSECONDS = 'microseconds'
    """
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
