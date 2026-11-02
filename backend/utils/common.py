# -*- coding: utf-8 -*-
"""
公共通用工具函数
"""
import re
from django.http import QueryDict
from rest_framework.request import Request

# 常用手机号正则
REGEX_MOBILE = r"^1[3-9]\d{9}$"

# 身份证正则
IDCARD_MOBILE = r"^[1-9]\d{5}(18|19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"


def re_api(api: str) -> str:
    """
    提取API路径部分，去除查询参数
    :param api: 请求的完整或相对路径
    :return: 规范化后的路径
    """
    if not api:
        return ""
    match = re.match(r'(/[^?]+)', api)
    return match.group(1) if match else api


def get_parameter_dic(request, *args, **kwargs) -> dict:
    """
    获取 GET 或 POST/PUT 请求参数字典
    :param request: Django/DRF Request 对象
    :return: 参数字典
    """
    if not isinstance(request, Request):
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params = query_params.dict()

    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params:
        return query_params
    return result_data if isinstance(result_data, dict) else {}
