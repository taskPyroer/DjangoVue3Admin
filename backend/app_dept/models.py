from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class Dept(BaseModel):
    dept_name = models.CharField(max_length=64, verbose_name="部门名称", help_text="部门名称")
    dept_key = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name="关联字符", help_text="关联字符")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    leader = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    IS_STATUS = (
        ('0', "正常"),
        ('1', "停用"),
    )
    status = models.CharField(choices=IS_STATUS, max_length=1, default='0', verbose_name="部门状态（0正常 1停用）", help_text="部门状态（0正常 1停用）")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级部门",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级部门",
    )

    class Meta:
        unique_together = ["dept_name", "dept_key"]
        db_table = table_prefix + "dept"
        verbose_name = "系统-部门表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)