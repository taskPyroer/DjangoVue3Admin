# -*- coding: utf-8 -*-
from collections import OrderedDict

from django.core import paginator
from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.response import Response
from django.core.paginator import InvalidPage


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "pageSize"
    max_page_size = 999
    django_paginator_class = DjangoPaginator

    def get_page_size(self, request):
        """
        同时兼容 pageSize 与 limit 参数
        """
        val = request.query_params.get(self.page_size_query_param) or request.query_params.get('limit')
        if val is not None:
            try:
                return _positive_int(val, strict=True, cutoff=self.max_page_size)
            except (KeyError, ValueError):
                pass
        return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        """
        重写paginate_queryset让分页超过正常分页:由原来的400错误改为返回空列表
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)
        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            self.page = []

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        code = 200
        msg = 'success'
        current_page = getattr(self.page, 'number', 1) if self.page else 1
        page_size = int(self.get_page_size(self.request)) or 10
        total = self.page.paginator.count if getattr(self.page, 'paginator', None) else 0
        res = {
            "page": current_page,
            "total": total,
            "pageSize": page_size,
            "limit": page_size,
            "data": data
        }
        if not data:
            code = 200
            msg = "暂无数据"
            res['data'] = []

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('data', res),
        ]))
