"""
Time:     2023/12/6 17:09
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     serializer
Describe: 信息中心数据序列化
"""
from rest_framework import serializers
from django_restql.fields import DynamicSerializerMethodField
from app_message.models import MessageCenter
from app_message.models import MessageCenterTargetUser
from app_user.models import Users
from application.websocketConfig import websocket_push
from utils.serializers import CustomModelSerializer


class MessageCenterSerializer(CustomModelSerializer):
    """
    消息中心-序列化器
    """
    role_info = DynamicSerializerMethodField()
    user_info = DynamicSerializerMethodField()
    dept_info = DynamicSerializerMethodField()
    is_read = serializers.BooleanField(read_only=True, source='target_user__is_read')

    def get_role_info(self, instance, parsed_query):
        roles = instance.target_role.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from app_role.serializers import RoleSerializer
        serializer = RoleSerializer(
            roles,
            many=True,
            # parsed_query=parsed_query
        )
        return serializer.data

    def get_user_info(self, instance, parsed_query):
        users = instance.target_user.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from app_user.serializers import UserSerializer
        serializer = UserSerializer(
            users,
            many=True,
            # parsed_query=parsed_query
        )
        return serializer.data

    def get_dept_info(self, instance, parsed_query):
        dept = instance.target_dept.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from app_dept.serializers import DeptSerializer
        serializer = DeptSerializer(
            dept,
            many=True,
            # parsed_query=parsed_query
        )
        return serializer.data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserSerializer(CustomModelSerializer):
    """
    目标用户序列化器-序列化器
    """

    class Meta:
        model = MessageCenterTargetUser
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserListSerializer(CustomModelSerializer):
    """
    目标用户列表序列化器-序列化器
    """
    is_read = serializers.SerializerMethodField()

    def get_is_read(self, instance):
        user_id = self.request.user.id
        message_center_id = instance.id
        queryset = MessageCenterTargetUser.objects.filter(messagecenter__id=message_center_id, users_id=user_id).first()
        if queryset:
            return queryset.is_read
        return False

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterCreateSerializer(CustomModelSerializer):
    """
    消息中心-新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        initial_data = self.initial_data
        target_type = initial_data.get('target_type')
        print(initial_data)
        # 在保存之前,根据目标类型,把目标用户查询出来并保存
        users = initial_data.get('target_user', [])
        if target_type in ['1']:  # 按角色
            target_role = initial_data.get('target_role', [])
            users = Users.objects.filter(role__id__in=target_role).values_list('id', flat=True)
        if target_type in ['2']:  # 按部门
            target_dept = initial_data.get('target_dept', [])
            users = Users.objects.filter(dept__id__in=target_dept).values_list('id', flat=True)
        if target_type in ['3']:  # 系统通知
            users = Users.objects.values_list('id', flat=True)
            websocket_push("PaoAdmin", message={"sender": 'system', "contentType": 'SYSTEM',
                                                "content": '您有一条新消息~', "refresh_unread": True})
        print(users)
        targetuser_data = []
        for user in users:
            targetuser_data.append({
                "messagecenter": data.id,
                "users": user
            })
            if target_type in ['0', '1', '2']:
                room_name = f"user_{user}"
                print("room_name", room_name)
                websocket_push(room_name, message={"sender": 'system', "contentType": 'SYSTEM',
                                                   "content": '您有一条新消息~', "refresh_unread": True})
        targetuser_instance = MessageCenterTargetUserSerializer(data=targetuser_data, many=True, request=self.request)
        targetuser_instance.is_valid(raise_exception=True)
        targetuser_instance.save()
        return data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]
