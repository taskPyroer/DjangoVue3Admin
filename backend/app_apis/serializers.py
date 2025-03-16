"""
Time:     2023/8/23 16:37
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe:
"""

from app_apis.models import APIS
from utils.serializers import CustomModelSerializer


class ApiSerializer(CustomModelSerializer):
    """
    API管理-序列化器
    """
    class Meta:
        model = APIS
        fields = "__all__"
        read_only_fields = ["id"]