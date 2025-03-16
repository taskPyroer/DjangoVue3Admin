"""
Time:     2023/8/23 16:37
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe: 
"""

from app_operation_log.models import OperationLog
from utils.serializers import CustomModelSerializer


class OperationLogSerializer(CustomModelSerializer):
    """
    操作日志-序列化器
    """

    class Meta:
        model = OperationLog
        fields = "__all__"
        read_only_fields = ["id"]


class OperationLogCreateUpdateSerializer(CustomModelSerializer):
    """
    操作日志  创建/更新时的列化器
    """

    class Meta:
        model = OperationLog
        fields = '__all__'
