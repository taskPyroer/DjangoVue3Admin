from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class Menu(BaseModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.PROTECT,
        verbose_name="上级菜单",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="上级菜单",
    )
    icon = models.CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    menu_name = models.CharField(max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    path = models.CharField(max_length=64, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    IS_IFRAME_CHOICES = (
        ('0', "是"),
        ('1', "否"),
    )
    is_iframe = models.CharField(choices=IS_IFRAME_CHOICES, max_length=1, null=True, blank=True, verbose_name="是否内嵌", help_text="是否内嵌")
    is_link = models.CharField(max_length=225, verbose_name="是否超级链接", null=True, blank=True, help_text="是否超级链接")
    MENU_TYPE_CHOICES = (
        (u"M", u"目录"),
        (u"C", u"菜单"),
        (u"F", u"按钮"),
    )
    menu_type = models.CharField(max_length=1, choices=MENU_TYPE_CHOICES, verbose_name="菜单类型（M目录 C菜单 F按钮）", help_text="菜单类型（M目录 C菜单 F按钮）")
    IS_HIDE_CHOICES = (
        ('0', "显示"),
        ('1', "隐藏"),
    )
    is_hide = models.CharField(max_length=1, choices=IS_HIDE_CHOICES, null=True, blank=True, verbose_name="显示状态（0显示 1隐藏）",
                               help_text="显示状态（0显示 1隐藏）")
    is_keep_alive = models.CharField(max_length=1, choices=IS_HIDE_CHOICES, null=True, blank=True, verbose_name="是否缓存组件状态（0是 1否）",
                                             help_text="是否缓存组件状态（0是 1否）")
    is_affix = models.CharField(max_length=1, choices=IS_HIDE_CHOICES, null=True, blank=True, verbose_name="是否固定在 tagsView 栏上（0是 1否）",
                                        help_text="是否固定在 tagsView 栏上（0是 1否）")
    permission = models.CharField(max_length=32, verbose_name="权限标识", null=True, blank=True, help_text="权限标识")
    IS_STATUS = (
        ('0', "正常"),
        ('1', "停用"),
    )
    status = models.CharField(max_length=1, choices=IS_STATUS, default='0', verbose_name="菜单状态（0正常 1停用）", help_text="菜单状态（0正常 1停用）")
    remark = models.CharField(max_length=150, null=True, blank=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + "menu"
        verbose_name = "系统-菜单表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)