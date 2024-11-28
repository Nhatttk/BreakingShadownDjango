import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *
from channels.db import database_sync_to_async
import datetime

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'private_chat_{self.chat_id}'

        # Tham gia nhóm
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Rời nhóm
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']

        chat = await database_sync_to_async(PrivateChat.objects.get)(id=self.chat_id)
        sender = await database_sync_to_async(Profile.objects.get)(user=sender_id)
        user = await database_sync_to_async(User.objects.get)(id=sender_id)
        new_message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            sender=sender,
            content=message
        )
        print(sender.avatar)
        message_data = {
            'chat': self.chat_id,
            'sender': {
                "address": sender.address,
                "phone": sender.phone,
                "avatar": sender.avatar.url,
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            },
            'content': message,
            'timestamp': ""
        }
        print("message_data: ", message_data)


        # Gửi tin nhắn tới nhóm
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message_data': message_data
            }
        )

    async def chat_message(self, event):
        message = event['message_data']

        # Gửi tin nhắn tới WebSocket
        await self.send(text_data=json.dumps({
            'message_data': message
        }))
