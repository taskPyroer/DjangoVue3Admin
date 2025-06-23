from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class Example(BaseModel):
    """
    示例模型 - 基础增删改查
    """
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    content = models.TextField(verbose_name="内容", help_text="内容", null=True, blank=True)
    category = models.CharField(max_length=50, verbose_name="分类", help_text="分类", null=True, blank=True)
    STATUS_CHOICES = (
        ("0", "正常"),
        ("1", "停用"),
    )
    status = models.CharField(
        max_length=1, 
        choices=STATUS_CHOICES, 
        default='0', 
        verbose_name="状态（0正常 1停用）", 
        help_text="状态（0正常 1停用）"
    )

    class Meta:
        db_table = table_prefix + "example"
        verbose_name = "系统-示例表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)

    def __str__(self):
        return self.title
