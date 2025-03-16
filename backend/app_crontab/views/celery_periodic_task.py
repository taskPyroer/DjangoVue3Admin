"""
Time:     2023/11/21 15:28
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     celery_periodic_task
Describe: 
"""
import json

from django.db import transaction
from django_celery_beat.models import PeriodicTask, CrontabSchedule, cronexp, PeriodicTasks, IntervalSchedule
from django_celery_results.models import TaskResult
from rest_framework import serializers

from app_crontab.filters import CeleryPeriodicTaskFilterSet
from app_crontab.views.celery_crontab_schedule import CrontabScheduleSerializer
from app_crontab.views.celery_interval_schedule import IntervalScheduleSerializer
from application import settings
from utils.common import get_parameter_dic
from utils.exception import APIException

from utils.json_response import SuccessResponse, DetailResponse, ErrorResponse
from utils.serializers import CustomModelSerializer
from utils.viewset import CustomModelViewSet

# CrontabSchedule的timezone属性已经不再使用或者不重要，因此不需要在字符串表示形式中显示出来
CrontabSchedule.__str__ = lambda self: '{0} {1} {2} {3} {4}'.format(
    cronexp(self.minute), cronexp(self.hour),
    cronexp(self.day_of_month), cronexp(self.month_of_year),
    cronexp(self.day_of_week)
)


def cronConvert(cron):
    """
    解析cron表达式为字典形式
    :param cron: * * * * * 分、时、天、月、周
    :return:
    """
    cron = cron.split(" ")
    result = {
        "minute": cron[0],
        "hour": cron[1],
        "day": cron[2],
        "month": cron[3],
        "week": cron[4]
    }
    return result


def get_task_list():
    """
    获取本地所有app目录中所有的tasks任务文件中“cron_job_”开头的任务方法
    :return:
    """
    task_list = []
    task_dict_list = []
    for app in settings.INSTALLED_APPS:
        try:
            exec(f"""
from {app} import tasks
for t in [i for i in dir(tasks) if i.startswith('cron_job_')]:
    task_dict = dict()
    task_dict['label'] = '{app}.tasks.' + t
    task_dict['value'] = '{app}.tasks.' + t
    task_list.append('{app}.tasks.' + t)
    task_dict_list.append(task_dict)
                """)
        except ImportError:
            pass
    return {'task_list': task_list, 'task_dict_list': task_dict_list}


class PeriodicTaskSerializer(CustomModelSerializer):
    crontab = serializers.StringRelatedField(read_only=True)
    crontab_id = serializers.SerializerMethodField(read_only=True)
    interval = serializers.SerializerMethodField(read_only=True)
    interval_id = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    def get_crontab_id(self, obj):
        return obj.crontab_id

    def get_interval(self, obj):
        if obj.interval_id:
            return {
                'every': obj.interval.every,
                'period': obj.interval.period
            }
        else:
            return None

    def get_interval_id(self, obj):
        return obj.interval_id

    def get_type(self, obj):
        """
        type=0(间隔任务)/type=1(周期任务)
        """
        type = 0
        if obj.crontab_id:
            type = 1
        return type

    class Meta:
        model = PeriodicTask
        read_only_fields = ["id"]
        fields = '__all__'


class PeriodicTaskCreateUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = PeriodicTask
        read_only_fields = ["id", "total_run_count", "date_changed"]
        fields = '__all__'


class PeriodicTaskModelViewSet(CustomModelViewSet):
    """
    任务数据模型
    """
    queryset = PeriodicTask.objects.exclude(name="celery.backend_cleanup")
    serializer_class = PeriodicTaskSerializer
    create_serializer_class = PeriodicTaskCreateUpdateSerializer
    update_serializer_class = PeriodicTaskCreateUpdateSerializer
    filterset_class = CeleryPeriodicTaskFilterSet
    ordering = ['-date_changed']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        body_data = request.data.copy()
        if 'kwargs' in body_data:
            body_data['kwargs'] = json.dumps(body_data['kwargs'], ensure_ascii=False)
        # body_data['args'] = json.dumps(body_data['args'])

        type = int(body_data.pop('type'))
        if type not in [0, 1]:
            return ErrorResponse(msg="type类型错误")
        if type == 1:  # 周期任务
            body_data.pop('interval')
            cron = body_data.get('crontab')
            cron_dict = cronConvert(cron)
            minute = cron_dict["minute"]
            hour = cron_dict["hour"]
            day = cron_dict["day"]
            month = cron_dict["month"]
            week = cron_dict["week"]
            cron_data = {
                'minute': minute,
                'hour': hour,
                'day_of_week': week,
                'day_of_month': day,
                'month_of_year': month
            }
            task = body_data.get('task')
            task_list = get_task_list()
            task_list = task_list.get('task_list')
            if task in task_list:
                # 添加crontab
                serializer = CrontabScheduleSerializer(data=cron_data, request=request)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                # 添加任务
                body_data['crontab'] = serializer.data.get('id')
                body_data['enabled'] = False  # 新建任务默认不启用

                serializer = self.get_serializer(data=body_data, request=request)
                res = serializer.is_valid()
                if not res:
                    raise APIException(message={"msg": f"添加失败，已经有一个名为 {body_data['name']} 的任务了"}, code=400)
                self.perform_create(serializer)
                result = serializer.data
                task_obj = PeriodicTask.objects.get(id=result.get('id'))
                PeriodicTasks.changed(task_obj)
                return DetailResponse(msg="添加成功", data=result)
            else:
                return ErrorResponse(msg="没有该任务方法，请先添加", data=None)
        else:  # 间隔任务
            # body_data.pop('crontab')
            interval = body_data.get('interval')
            every = interval['every']
            period = interval['period']
            if not all([every, period]):
                return ErrorResponse(msg="间隔时间错误")
            task = body_data.get('task')
            task_list = get_task_list()
            task_list = task_list.get('task_list')
            if task in task_list:
                # 添加crontab
                serializer = IntervalScheduleSerializer(data=interval, request=request)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

                # 添加任务
                body_data['interval'] = serializer.data.get('id')
                body_data['enabled'] = False  # 新建任务默认不启用
                serializer = self.get_serializer(data=body_data, request=request)
                res = serializer.is_valid()
                if not res:
                    raise APIException(message={"msg": f"添加失败，已经有一个名为 {body_data['name']} 的任务了"}, code=400)
                self.perform_create(serializer)
                result = serializer.data
                task_obj = PeriodicTask.objects.get(id=result.get('id'))
                PeriodicTasks.changed(task_obj)
                return DetailResponse(msg="添加成功", data=result)
            else:
                return ErrorResponse(msg="没有该任务方法，请先添加", data=None)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        body_data = request.data.copy()
        type = int(body_data.pop('type'))
        if type not in [0, 1]:
            return ErrorResponse(msg="type类型错误")
        if type == 1:
            body_data.pop('interval')
            body_data.pop('interval_id')
            cron = body_data.get('crontab')
            cron_id = body_data.get('crontab_id')
            cron_dict = cronConvert(cron)
            minute = cron_dict["minute"]
            hour = cron_dict["hour"]
            day = cron_dict["day"]
            month = cron_dict["month"]
            week = cron_dict["week"]
            cron_data = {
                'minute': minute,
                'hour': hour,
                'day_of_week': week,
                'day_of_month': day,
                'month_of_year': month
            }
            task = body_data.get('task')
            task_list = get_task_list()
            task_list = task_list.get('task_list')
            if task in task_list:
                # 编辑crontab
                cond_instance = CrontabSchedule.objects.filter(id=cron_id).first()
                oldcron = '{0} {1} {2} {3} {4}'.format(
                    cronexp(cond_instance.minute), cronexp(cond_instance.hour),
                    cronexp(cond_instance.day_of_month), cronexp(cond_instance.month_of_year),
                    cronexp(cond_instance.day_of_week)
                )
                if cron.strip() == oldcron:
                    body_data['crontab'] = cron_id
                else:
                    cron_data['id'] = cron_id
                    serializer = CrontabScheduleSerializer(cond_instance, data=cron_data, request=request)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    body_data['crontab'] = cond_instance.id
                header = {}
                header['periodic_task_name'] = body_data['name']
                header['task_name'] = body_data['task']
                body_data['headers'] = json.dumps(header)
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer1 = self.get_serializer(instance, data=body_data, request=request, partial=partial)
                serializer1.is_valid(raise_exception=True)
                self.perform_update(serializer1)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
                task_obj = PeriodicTask.objects.get(id=instance.id)
                PeriodicTasks.changed(task_obj)
                return DetailResponse(data=serializer1.data, msg="更新成功")
            else:
                return ErrorResponse(msg="没有该任务方法，请先添加", data=None)
        else:
            body_data.pop('crontab')
            body_data.pop('crontab_id')
            interval = body_data.get('interval')
            interval_id = body_data.get('interval_id')
            every = interval['every']
            period = interval['period']
            if not all([every, period]):
                return ErrorResponse(msg="间隔时间错误")
            task = body_data.get('task')
            task_list = get_task_list()
            task_list = task_list.get('task_list')
            if task in task_list:
                # 编辑crontab
                interval_instance = IntervalSchedule.objects.filter(id=interval_id).first()
                if interval_instance.every == every and interval_instance.period == period:
                    body_data['interval'] = interval_id
                else:
                    interval['id'] = interval_id
                    serializer = IntervalScheduleSerializer(interval_instance, data=interval, request=request)
                    serializer.is_valid(raise_exception=True)
                    self.perform_update(serializer)
                    body_data['interval'] = interval_instance.id
                partial = kwargs.pop('partial', False)
                instance = self.get_object()
                serializer1 = self.get_serializer(instance, data=body_data, request=request, partial=partial)
                serializer1.is_valid(raise_exception=True)
                self.perform_update(serializer1)

                if getattr(instance, '_prefetched_objects_cache', None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}
                task_obj = PeriodicTask.objects.get(id=instance.id)
                PeriodicTasks.changed(task_obj)
                return DetailResponse(data=serializer1.data, msg="更新成功")
            else:
                return ErrorResponse(msg="没有该任务方法，请先添加", data=None)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object_list()
        task_result_ids_to_delete = []
        for i in instance:
            if i.crontab_id:
                i.crontab.delete()
            if i.interval_id:
                i.interval.delete()
            # Collect the TaskResult ids to delete later
            task_result_ids_to_delete.append(i.name)

        # Delete the TaskResult objects that meet the condition
        TaskResult.objects.filter(periodic_task_name__in=task_result_ids_to_delete).delete()

        self.perform_destroy(instance)
        return DetailResponse(data=[], msg="删除成功")

    def tasklist(self, request, *args, **kwargs):
        """获取本地tasks任务所有方法"""
        result = get_task_list()
        task_list = result.get('task_dict_list')
        return SuccessResponse(msg='获取成功', data=task_list, total=len(task_list))

    def taskenabled(self, request, *args, **kwargs):
        """开始、暂停任务"""
        instance = self.get_object()
        instance.enabled = get_parameter_dic(request).get('enabled', False)
        instance.save()
        PeriodicTasks.changed(instance)
        return DetailResponse(msg="修改成功")
