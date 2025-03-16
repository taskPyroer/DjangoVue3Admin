"""
Time:     2023/9/11 15:00
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     urls
Describe:
"""
from rest_framework import routers

from app_dict.views import DictDataViewSet, DictTypeViewSet

system_url = routers.SimpleRouter()
system_url.register(r'dict-type', DictTypeViewSet)
system_url.register(r'dict-data', DictDataViewSet)

urlpatterns = [

]
urlpatterns += system_url.urls