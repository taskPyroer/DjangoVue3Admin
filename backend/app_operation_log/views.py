# Create your views here.
import os
import subprocess
import platform
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
        获取日志
        """
        type_log = request.GET.get('type_log', 'server')
        num_lines = request.GET.get('num_lines')
        keyword = request.GET.get('keyword')

        if type_log == 'server':
            log_file = os.path.join(BASE_DIR, 'logs', 'server.log')
        elif type_log == 'error':
            log_file = os.path.join(BASE_DIR, 'logs', 'error.log')
        else:
            # 默认读取 server.log
            log_file = os.path.join(BASE_DIR, 'logs', 'server.log')
        # 构建命令
        plat = platform.system().lower()
        if plat == 'windows':
            command = f'powershell -Command "Get-Content'
            if num_lines:
                command += f' -Tail {num_lines}'
        else:
            command = f'cat {log_file}'
            if num_lines:
                command += f' | tail -n {num_lines}'
        command += f' {log_file}"'

        # 执行命令
        p = subprocess.run(command, capture_output=True, text=True, shell=True, check=True)
        content = p.stdout
        # 如果提供了关键词，则进行搜索过滤
        if keyword:
            filtered_content = filter(lambda line: keyword in line, content.split('\n'))
            content = '\n'.join(filtered_content)

        return DetailResponse(data=content)
