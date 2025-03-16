"""
Time:     2023/8/23 11:09
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe: 
"""
from import_export.fields import Field
from import_export import resources
from app_post.models import Post
from utils.serializers import CustomModelSerializer


class PostSerializers(CustomModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["id"]


class PostResource(resources.ModelResource):
    id = Field(attribute='id', column_name=Post.id.field.verbose_name)
    post_name = Field(attribute='post_name', column_name=Post.post_name.field.verbose_name)
    post_code = Field(attribute='post_code', column_name=Post.post_code.field.verbose_name)
    sort = Field(attribute='sort', column_name=Post.sort.field.verbose_name)
    status = Field(attribute='status', column_name=Post.status.field.verbose_name)
    remark = Field(attribute='remark', column_name=Post.remark.field.verbose_name)
    update_datetime = Field(attribute='update_datetime', column_name=Post.update_datetime.field.verbose_name)
    create_datetime = Field(attribute='create_datetime', column_name=Post.create_datetime.field.verbose_name)

    class Meta:
        model = Post
        fields = ('id', 'post_name', 'post_code', 'sort', 'status', 'remark', 'update_datetime', 'create_datetime')
        export_order = fields