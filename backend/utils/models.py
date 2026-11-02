"""
Time:     2023/8/6 16:07
Author:   公众号【布鲁的Python之旅】
Version:  V 0.1
File:
Describe: 公共基础model类
"""
import time

from django.db import models
from application import settings

table_prefix = "sys_"  # 数据库表名前缀


class SnowflakeGenerator:
    """
    轻量级高并发雪花ID生成器 (41位时间戳 + 10位工作节点 + 12位序号)
    """
    def __init__(self, worker_id=1):
        self.worker_id = worker_id & 0x3FF
        self.sequence = 0
        self.last_timestamp = -1
        self.epoch = 1609459200000  # 2021-01-01 起始基准时间戳

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def get_id(self):
        timestamp = self._get_timestamp()
        if timestamp < self.last_timestamp:
            # 时钟回拨保护
            timestamp = self.last_timestamp

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFFF
            if self.sequence == 0:
                # 单毫秒溢出，等待下一毫秒
                while timestamp <= self.last_timestamp:
                    timestamp = self._get_timestamp()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        return ((timestamp - self.epoch) << 22) | (self.worker_id << 12) | self.sequence


_snowflake = SnowflakeGenerator(worker_id=1)


class SnowflakeIDField(models.BigIntegerField):
    """
    雪花主键字段：确保新增且未指定ID时自动生成，更新时绝对不篡改主键
    """
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if add and not value:
            value = _snowflake.get_id()
            setattr(model_instance, self.attname, value)
        return value


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
