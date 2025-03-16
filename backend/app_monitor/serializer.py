"""
Time:     2023/12/1 9:41
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializer
Describe: 
"""
from app_monitor.models import MonitorManage
from utils.serializers import CustomModelSerializer


class MonitorManageSerializer(CustomModelSerializer):
    """
    服务器监控 简单序列化器
    """

    class Meta:
        model = MonitorManage
        # fields = "__all__"
        exclude = ['dept_belong_id', 'modifier', 'creator', 'description']
        read_only_fields = ["id"]
