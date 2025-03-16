from django.db import models

# Create your models here.
from utils.models import BaseModel, table_prefix


class Post(BaseModel):
    post_name = models.CharField(null=False, max_length=64, verbose_name="岗位名称", help_text="岗位名称")
    post_code = models.CharField(max_length=32, verbose_name="岗位代码", help_text="岗位代码")
    sort = models.IntegerField(default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        ('0', "在职"),
        ('1', "离职"),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0', verbose_name="岗位状态（0在职 1离职）", help_text="岗位状态（0在职 1离职）")
    remark = models.CharField(max_length=150, null=True, blank=True, verbose_name="备注", help_text="备注")

    class Meta:
        unique_together = ["post_name", "post_code"]
        db_table = table_prefix + "post"
        verbose_name = "系统-岗位表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)