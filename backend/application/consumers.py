"""
Time:     2023/12/5 16:16
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     consumers
Describe: 
"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)

        # 加入房间
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 离开房间
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 接收来自WebSocket的消息
    async def receive(self, text_data):
        # 发送消息到房间组
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': json.dumps({"message": text_data}, ensure_ascii=False)
            }
        )

    # 接收来自房间组的消息
    async def chat_message(self, event):
        message = event['message']
        print("<<", message)
        # 发送消息到WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


def websocket_push(room_name, message):
    channel_layer = get_channel_layer()
    print(room_name, message)
    async_to_sync(channel_layer.group_send)(
        'chat_%s' % room_name,
        {
            'type': 'chat_message',
            'message': json.dumps(message, ensure_ascii=False)
        }
    )
