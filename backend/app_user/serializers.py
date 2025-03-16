"""
Time:     2023/8/31 16:38
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializers
Describe: 
"""
import re
from import_export.fields import Field
from import_export import resources
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from app_post.models import Post
from app_role.models import Role
from app_dept.models import Dept
from app_user.models import Users
from utils.common import REGEX_MOBILE
from utils.serializers import CustomModelSerializer
from utils.validator import CustomUniqueValidator, CustomValidationError


class UserSerializer(CustomModelSerializer):
    """
    用户-序列化器
    """
    dept_name = serializers.CharField(source='dept.dept_name', read_only=True)

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ["password"]


class UserCreateSerializer(CustomModelSerializer):
    """
    用户信息修改/更新-序列化器
    """
    password = serializers.CharField(required=False, default=make_password("123456"))
    username = serializers.CharField(
        max_length=50,
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    nickname = serializers.CharField(
        max_length=50,
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="用户昵称必须唯一")])
    phone = serializers.CharField(
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="手机号必须唯一")],
        allow_blank=True)

    def validate_phone(self, value):
        if not re.match(REGEX_MOBILE, value):
            raise CustomValidationError('请输入一个有效的手机号码')
        return value

    def create(self, validated_data):
        if 'password' in validated_data.keys():
            if validated_data['password']:
                validated_data['password'] = make_password(validated_data['password'])

        return super().create(validated_data)

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    """
    用户个人信息修改-序列化器
    """
    phone = serializers.CharField(
        validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="手机号必须唯一")],
        allow_blank=True)

    def validate_phone(self, value):
        if not re.match(REGEX_MOBILE, value):
            raise serializers.ValidationError('请输入一个有效的手机号码')
        return value

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Users
        fields = ['email', 'avatar', 'nickname', 'gender']


class UserResource(resources.ModelResource):
    id = Field(attribute='id', column_name=Users.id.field.verbose_name)
    status = Field(attribute='status', column_name=Users.status.field.verbose_name)
    username = Field(attribute='username', column_name=Users.username.field.verbose_name)
    nickname = Field(attribute='nickname', column_name=Users.nickname.field.verbose_name)
    employee_no = Field(attribute='employee_no', column_name=Users.employee_no.field.verbose_name)
    email = Field(attribute='email', column_name=Users.email.field.verbose_name)
    phone = Field(attribute='phone', column_name=Users.phone.field.verbose_name)
    gender = Field(attribute='gender', column_name=Users.gender.field.verbose_name)
    post = Field(
        column_name='关联岗位',
        attribute='post',
        widget=ManyToManyWidget(Post, field='post_name')
    )
    role = Field(
        column_name='关联角色',
        attribute='role',
        widget=ManyToManyWidget(Role, field='role_name')
    )
    dept = Field(
        column_name='所属部门',
        attribute='dept',
        widget=ForeignKeyWidget(Dept, field='dept_name')
    )
    remark = Field(attribute='remark', column_name=Users.remark.field.verbose_name)
    update_datetime = Field(attribute='update_datetime', column_name=Users.update_datetime.field.verbose_name)
    create_datetime = Field(attribute='create_datetime', column_name=Users.create_datetime.field.verbose_name)

    class Meta:
        model = Users
        fields = ('id', 'status', 'username', 'nickname', 'employee_no', 'email', 'phone', 'gender', 'post', 'role', 'dept', 'remark',
                  'update_datetime', 'create_datetime')
        export_order = fields