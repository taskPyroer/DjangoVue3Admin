from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class APIS(BaseModel):
    path = models.CharField(max_length=64, verbose_name="路由地址", help_text="路由地址")
    description = models.CharField(max_length=150, null=True, blank=True, verbose_name="api中文描述", help_text="api中文描述")
    api_group = models.CharField(max_length=150, verbose_name="api组", help_text="api组")
    METHOD_CHOICES = (
        (u"POST", u"创建"),
        (u"GET", u"查看"),
        (u"PUT", u"更新"),
        (u"DELETE", u"删除"),
    )
    method = models.CharField(max_length=6, choices=METHOD_CHOICES, default='POST', verbose_name='创建POST(默认)|查看GET|更新PUT|删除DELETE',
                              help_text="创建POST(默认)|查看GET|更新PUT|删除DELETE")
    IS_STATUS = (
        ('0', "需要"),
        ('1', "不需要"),
    )
    enable_datasource = models.CharField(max_length=1, choices=IS_STATUS, default='0', verbose_name="激活数据权限", help_text="激活数据权限", db_index=True)

    class Meta:
        unique_together = ["path", "api_group", "method"]
        db_table = table_prefix + "apis"
        verbose_name = '系统-API接口表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)