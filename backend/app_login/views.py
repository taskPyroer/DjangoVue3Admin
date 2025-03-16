"""
Time:     2023/9/11 14:51
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:
Describe:
"""
import base64

from captcha.views import CaptchaStore, captcha_image

# Create your views here.
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from app_login.serializer import LoginSerializer
from utils.json_response import DetailResponse


class CaptchaView(APIView):
    """
    获取图片验证码
    """

    def get(self, request):
        hashkey = CaptchaStore.generate_key()
        id = CaptchaStore.objects.filter(hashkey=hashkey).first().id
        imgage = captcha_image(request, hashkey)
        # 将图片转换为base64
        image_base = base64.b64encode(imgage.content)
        json_data = {"key": id, "image_base": "data:image/png;base64," + image_base.decode('utf-8')}
        return DetailResponse(data=json_data)


class LoginView(TokenObtainPairView):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = []
