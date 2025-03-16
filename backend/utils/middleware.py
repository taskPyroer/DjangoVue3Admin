"""
Time:     2023/12/3 14:16
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     middleware
Describe: 自定义中间件
"""
import json

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

from app_operation_log.models import OperationLog
from application.settings import IS_SINGLE_TOKEN
from utils.request_util import get_request_ip, get_request_data, get_request_path, get_request_user, get_os, get_browser, get_verbose_name


class ApiLoggingMiddleware(MiddlewareMixin):
    """
    用于记录API访问日志中间件
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.enable = getattr(settings, 'API_LOG_ENABLE', None) or False
        self.methods = getattr(settings, 'API_LOG_METHODS', None) or set()
        self.operation_log_id = None

    @classmethod
    def __handle_request(cls, request):
        request.request_ip = get_request_ip(request)
        request.request_data = get_request_data(request)
        request.request_path = get_request_path(request)

    def __handle_response(self, request, response):
        # request_data,request_ip由PermissionInterfaceMiddleware中间件中添加的属性
        body = getattr(request, 'request_data', {})
        # 请求含有password则用*替换掉(暂时先用于所有接口的password请求参数)
        if isinstance(body, dict) and body.get('password', ''):
            body['password'] = '*' * len(body['password'])
        if not hasattr(response, 'data') or not isinstance(response.data, dict):
            response.data = {}
        try:
            if not response.data and response.content:
                content = json.loads(response.content.decode())
                response.data = content if isinstance(content, dict) else {}
        except Exception:
            return
        user = get_request_user(request)
        info = {
            'request_ip': getattr(request, 'request_ip', 'unknown'),
            'creator': user if not isinstance(user, AnonymousUser) else None,
            'request_method': request.method,
            'request_path': request.request_path,
            'request_body': body,
            'response_code': response.data.get('code'),
            'request_os': get_os(request),
            'request_browser': get_browser(request),
            'request_msg': request.session.get('request_msg'),
            'status': True if response.data.get('code') in [200, ] else False,
            'json_result': {"code": response.data.get('code', ''), "msg": response.data.get('msg', '')},
        }
        operation_log, creat = OperationLog.objects.update_or_create(defaults=info, id=self.operation_log_id)
        if not operation_log.request_modular and settings.API_MODEL_MAP.get(request.request_path, None):
            operation_log.request_modular = settings.API_MODEL_MAP[request.request_path]
            operation_log.save()

    def process_view(self, request, view_func, view_args, view_kwargs):
        if hasattr(view_func, 'cls') and hasattr(view_func.cls, 'queryset'):
            if self.enable:
                if self.methods == 'ALL' or request.method in self.methods:
                    log = OperationLog(request_modular=get_verbose_name(view_func.cls.queryset))
                    log.save()
                    self.operation_log_id = log.id

        return

    def process_request(self, request):
        self.__handle_request(request)
        if IS_SINGLE_TOKEN:  # 保证设备登录的唯一性
            jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
            if jwt_token and 'JWT' in jwt_token and jwt_token.split('JWT ')[1] != 'null':
                error_data = {'msg': '身份认证已经过期，请重新登入', 'code': 401, 'data': ''}
                try:
                    user, token = JWTTokenUserAuthentication().authenticate(request)
                    redis_conn = get_redis_connection("singletoken")
                    k = "pao-single-token{}".format(user.id)
                    cache_token = redis_conn.get(k)
                    if cache_token:
                        if not str(token) == str(cache_token):
                            return HttpResponse(json.dumps(error_data), content_type='application/json', status=200, charset='utf-8')
                    else:
                        return HttpResponse(json.dumps(error_data), content_type='application/json', status=200, charset='utf-8')
                except Exception as e:
                    print(e)
                    return HttpResponse(json.dumps(error_data), content_type='application/json', status=200, charset='utf-8')

    def process_response(self, request, response):
        """
        主要请求处理完之后记录
        :param request:
        :param response:
        :return:
        """
        if self.enable:
            if self.methods == 'ALL' or request.method in self.methods:
                self.__handle_response(request, response)
        return response
