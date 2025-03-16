from django.shortcuts import render

# Create your views here.
from app_monitor.models import MonitorManage
from app_monitor.serializer import MonitorManageSerializer
from utils.json_response import DetailResponse
from utils.server.system import system
from utils.viewset import CustomModelViewSet


class MonitorManageViewSet(CustomModelViewSet):
    """
    前端用户服务器监控
    """
    queryset = MonitorManage.objects.all().order_by("create_datetime")
    serializer_class = MonitorManageSerializer

    def get_system_info(self, request):
        data = system().GetSystemAllInfo()
        return DetailResponse(data=data)
