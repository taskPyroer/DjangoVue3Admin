# Create your views here.
import collections
import os
from app_operation_log.filters import OperationLogTimeFilter
from app_operation_log.models import OperationLog
from app_operation_log.serializers import OperationLogSerializer
from application.settings import BASE_DIR
from utils.json_response import ErrorResponse, DetailResponse
from utils.viewset import CustomModelViewSet


class OperationLogViewSet(CustomModelViewSet):
    """
    操作日志接口
    """
    queryset = OperationLog.objects.all().order_by('-create_datetime')
    serializer_class = OperationLogSerializer
    filterset_class = OperationLogTimeFilter
    search_fields = ['request_modular', 'request_path', 'request_ip', 'request_os', 'request_body']

    def delete_all_logs(self, request):
        user = request.user
        if user.is_superuser:
            OperationLog.objects.all().delete()
            return DetailResponse(msg="清空成功")
        return ErrorResponse(msg="您没有权限执行此操作，需要超级管理员权限")

    def get_read_logs(self, request):
        """
        获取日志（纯Python逆序安全读取，杜绝命令注入）
        """
        type_log = request.GET.get('type_log', 'server')
        num_lines = request.GET.get('num_lines')
        keyword = request.GET.get('keyword')

        if type_log == 'error':
            log_file = os.path.join(BASE_DIR, 'logs', 'error.log')
        else:
            log_file = os.path.join(BASE_DIR, 'logs', 'server.log')

        if not os.path.exists(log_file):
            return DetailResponse(data="")

        try:
            limit = int(num_lines) if num_lines and str(num_lines).isdigit() else None
        except (ValueError, TypeError):
            limit = None

        try:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                if limit and limit > 0:
                    lines = list(collections.deque(f, maxlen=limit))
                else:
                    lines = f.readlines()

            if keyword:
                lines = [line for line in lines if keyword in line]

            content = ''.join(lines)
        except Exception as e:
            content = f"读取日志失败: {str(e)}"

        return DetailResponse(data=content)
