"""
Time:     2023/9/11 14:51
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe:
"""
from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class DictType(BaseModel):
    dict_name = models.CharField(max_length=64, unique=True, verbose_name="字典名称", help_text="字典名称")
    dict_type = models.CharField(max_length=64, unique=True, verbose_name="类型", help_text="类型")
    STATUS_CHOICES = (
        ("0", "正常"),
        ("1", "停用"),
    )
    status = models.CharField(max_length=1,choices=STATUS_CHOICES, default='0', verbose_name="字典状态（0正常 1停用）", help_text="字典状态（0正常 1停用）")
    remark = models.CharField(max_length=150, null=True, blank=True, verbose_name="备注", help_text="备注")

    class Meta:
        unique_together = ["dict_name", "dict_type"]
        db_table = table_prefix + "dict_type"
        verbose_name = '系统-字典类型'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


class DictData(BaseModel):
    sort = models.IntegerField(default=1, verbose_name="字典顺序", help_text="字典顺序")
    dict_label = models.CharField(max_length=64, verbose_name="字典标签", help_text="字典标签")
    dict_value = models.CharField(max_length=64, verbose_name="字典数值", help_text="字典数值")
    dict_type = models.CharField(max_length=64, verbose_name="类型", help_text="类型")
    STATUS_CHOICES = (
        ("0", "正常"),
        ("1", "停用"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0', verbose_name="字典状态（0正常 1停用）", help_text="字典状态（0正常 1停用）")
    remark = models.CharField(max_length=150, null=True, blank=True, verbose_name="备注", help_text="备注")

    class Meta:
        unique_together = ["dict_label", "dict_value", "dict_type"]
        db_table = table_prefix + "dict_data"
        verbose_name = '系统-字典数值'
        verbose_name_plural = verbose_name
        ordering = ('sort', '-create_datetime',)

