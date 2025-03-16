"""
Time:     2023/9/2 14:56
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializer
Describe:
"""
from datetime import datetime, timedelta

from captcha.models import CaptchaStore
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from app_user.models import Users
from application import settings
from application.settings import IS_SINGLE_TOKEN
from utils.validator import CustomValidationError


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """
    captcha = serializers.CharField(
        max_length=6, required=False, allow_null=True, allow_blank=True
    )

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {"no_active_account": _("账号/密码错误")}

    # 开启验证码验证
    def validate_captcha(self, captcha):
        self.image_code = CaptchaStore.objects.filter(id=self.initial_data['captchaKey']).first()
        five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        if self.image_code and five_minute_ago > self.image_code.expiration:
            self.image_code and self.image_code.delete()
            raise CustomValidationError('验证码过期')
        else:
            if self.image_code and (self.image_code.response == captcha or self.image_code.challenge == captcha):
                self.image_code and self.image_code.delete()
            else:
                self.image_code and self.image_code.delete()
                raise CustomValidationError("图片验证码错误")

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = Users.objects.filter(username=username).first()

        if not user:
            result = {
                "code": 400,
                "msg": "账号/密码不正确",
                "data": None
            }
            return result

        if user and not user.is_staff:  # 判断是否允许登录后台
            result = {
                "code": 400,
                "msg": "您没有权限登录后台",
                "data": None
            }

            return result

        if user and not user.is_active:
            result = {
                "code": 400,
                "msg": "该账号已被禁用,请联系管理员",
                "data": None
            }
            return result

        if user and user.check_password(password):  # check_password() 对明文进行加密,并验证
            data = super().validate(attrs)
            refresh = self.get_token(self.user)

            data['username'] = self.user.username
            data['userId'] = self.user.id
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            request = self.context.get('request')
            request.user = self.user
            # 缓存用户的jwt token
            if IS_SINGLE_TOKEN:  # 是否开启单点登录
                redis_conn = get_redis_connection("singletoken")
                k = "pao-single-token{}".format(user.id)
                TOKEN_EXPIRE_CONFIG = getattr(settings, 'SIMPLE_JWT', None)
                if TOKEN_EXPIRE_CONFIG:
                    TOKEN_EXPIRE = TOKEN_EXPIRE_CONFIG['ACCESS_TOKEN_LIFETIME']
                    redis_conn.set(k, data['access'], TOKEN_EXPIRE)
            result = {
                "code": 200,
                "msg": "请求成功",
                "data": data
            }
        else:
            result = {
                "code": 400,
                "msg": "账号/密码不正确",
                "data": None
            }
        return result