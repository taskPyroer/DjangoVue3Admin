
# Create your models here.
from django.db import models
from app_dept.models import Dept
from app_menu.models import Menu
from utils.models import BaseModel, table_prefix

class Role(BaseModel):
    role_name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    role_key = models.CharField(max_length=64, unique=True, verbose_name="角色代码", help_text="角色代码")
    IS_STATUS = (
        ('0', "正常"),
        ('1', "停用"),
    )
    status = models.CharField(max_length=1, choices=IS_STATUS, default='0', verbose_name="角色状态（0正常 1停用）", help_text="角色状态（0正常 1停用）")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    admin = models.BooleanField(default=False, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        ("1", "全部数据权限"),
        ("2", "自定数据权限"),
        ("3", "本部门数据权限"),
        ("4", "本部门及以下数据权限"),
        ("5", "仅本人数据权限")
    )
    data_scope = models.CharField(max_length=1, default='5', choices=DATASCOPE_CHOICES, verbose_name="数据权限范围", help_text="数据权限范围")
    remark = models.CharField(max_length=128, verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = models.ManyToManyField(to=Dept, verbose_name="数据权限-关联部门", db_constraint=False, help_text="数据权限-关联部门")
    menu = models.ManyToManyField(to=Menu, verbose_name="数据权限-关联菜单", db_constraint=False, help_text="数据权限-关联菜单")
    # api = models.TextField(verbose_name="数据权限-关联API", null=True, blank=True,help_text="数据权限-关联API")

    class Meta:
        db_table = table_prefix + "role"
        verbose_name = "系统-角色表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)