"""
Time:     2023/8/6 16:07
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:
Describe: 公共基础model类
"""
import secrets
import time

from django.db import models
from application import settings

table_prefix = "sys_"  # 数据库表名前缀


class SnowflakeIDField(models.BigIntegerField):
    """
    雪花id-生成16位
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_id(self):
        timestamp = int(time.time() * 1000)
        # 将时间戳缩小到合适的位数（例如，取后面的10位）
        timestamp = (timestamp - 1564454400000) % 10000000000
        return (timestamp << 6)  # 使用6位表示时间戳，剩余10位可根据需要分配给机器ID和序列号

    def pre_save(self, model_instance, add):
        snowflake_id = self.generate_id()
        setattr(model_instance, self.attname, snowflake_id)
        return snowflake_id

def generate_id():
    timestamp = int(time.perf_counter_ns())  # 获取纳秒级时间戳
    random_number = secrets.randbelow(10**4)  # 生成一个4位随机数
    id = str(timestamp) + str(random_number).zfill(6)  # 将时间戳和随机数拼接成ID，随机数左侧填充0
    return id


class BaseModel(models.Model):
    """
    基本模型,可直接继承使用，一般不需要使用审计字段的模型可以使用
    覆盖字段时, 字段名称请勿修改
    """
    # id = models.BigAutoField(primary_key=True, default=generate_id, help_text="Id", verbose_name="Id")
    id = SnowflakeIDField(primary_key=True)
    creator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_query_name='creator_query', null=True,
                                verbose_name='创建人', help_text="创建人", on_delete=models.SET_NULL,
                                db_constraint=False)
    modifier = models.CharField(max_length=255, null=True, blank=True, help_text="修改人", verbose_name="修改人")
    update_datetime = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')
    create_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')

    class Meta:
        abstract = True  # 表示该类是一个抽象类，只用来继承，不参与迁移操作
        verbose_name = '基本模型'
        verbose_name_plural = verbose_name
