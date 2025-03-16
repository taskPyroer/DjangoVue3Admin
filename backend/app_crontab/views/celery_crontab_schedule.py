"""
Time:     2023/11/21 11:07
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     celery_crontab_schedule
Describe: 指定某个时间执行定时任务的控制器 (例：每年的12月星期一的8:30)
"""
from django_celery_beat.models import CrontabSchedule

from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet


class CrontabScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = CrontabSchedule
        read_only_fields = ["id"]
        exclude = ('timezone',)
        # fields = '__all__'


class CrontabScheduleModelViewSet(CustomModelViewSet):
    """
    crontab 的周期性任务（同linux的crontab）

    minute="0" 分钟
    hour="*"   小时
    day_of_week="*" 每周的星期几
    day_of_month="10-15" 每月的某一天或间隔
    month_of_year="*"  每年的某一个月
    """
    queryset = CrontabSchedule.objects.all()
    serializer_class = CrontabScheduleSerializer
