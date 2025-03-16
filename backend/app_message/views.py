# Create your views here.
from app_message.models import MessageCenter, MessageCenterTargetUser
from app_message.serializer import MessageCenterSerializer, MessageCenterCreateSerializer, MessageCenterTargetUserListSerializer
from application.websocketConfig import websocket_push
from utils.json_response import DetailResponse, SuccessResponse
from utils.viewset import CustomModelViewSet


class MessageCenterViewSet(CustomModelViewSet):
    """
    消息中心接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = MessageCenter.objects.order_by('create_datetime')
    serializer_class = MessageCenterSerializer
    create_serializer_class = MessageCenterCreateSerializer
    filterset_fields = ['target_type']
    search_fields = ['title']
    extra_filter_backends = []

    def get_queryset(self):
        """
        这里重写查询全部，是针对获取我发布的信息
        """
        if self.action == 'list':
            return MessageCenter.objects.filter(creator=self.request.user.id).all()
        return MessageCenter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        重写查看
        """
        pk = kwargs.get('pk')
        user_id = self.request.user.id
        queryset = MessageCenterTargetUser.objects.filter(users__id=user_id, messagecenter__id=pk).first()
        if queryset:
            queryset.is_read = True
            queryset.save()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 主动推送消息
        room_name = f"user_{user_id}"
        websocket_push(room_name, message={"sender": 'system', "contentType": 'TEXT',
                                           "content": '您查看了一条消息~', "refresh_unread": True})
        return DetailResponse(data=serializer.data, msg="获取成功")

    def get_unread_msg(self, request):
        """
        获取未读消息数量
        """
        self_user_id = self.request.user.id
        count = MessageCenterTargetUser.objects.filter(users__id=self_user_id, is_read=False).count()
        return DetailResponse(data={"count": count}, msg="获取成功")

    def get_newest_msg(self, request):
        """
        获取最新的一条消息
        """
        self_user_id = self.request.user.id
        queryset = MessageCenterTargetUser.objects.filter(users__id=self_user_id).order_by('create_datetime').last()
        data = None
        if queryset:
            serializer = MessageCenterTargetUserListSerializer(queryset.messagecenter, many=False, request=request)
            data = serializer.data
        return DetailResponse(data=data, msg="获取成功")

    def get_self_receive(self, request):
        """
        获取接收到的消息
        """
        target_type = request.query_params.get('target_type')  # 从 URL 参数中获取 target_type
        title = request.query_params.get('search')  # 从 URL 参数中获取 search

        self_user_id = self.request.user.id
        queryset = MessageCenter.objects.filter(target_user__id=self_user_id)
        if target_type is not None:
            queryset = queryset.filter(target_type=target_type)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MessageCenterTargetUserListSerializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = MessageCenterTargetUserListSerializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")
