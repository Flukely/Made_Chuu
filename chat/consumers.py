import json
from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import *

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'

        # เข้าร่วมห้องแชท
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # ออกจากห้องแชท
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # รับข้อความจาก WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # บันทึกข้อความ
        await self.save_message(message)

        # ส่งข้อความไปยังกลุ่มห้องแชท
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # ส่งข้อความไปยัง WebSocket
    async def chat_message(self, event):
        message = event['message']

        # ส่งข้อความไปยัง WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def save_message(self, message):
        chat = Chat.objects.get(id=self.chat_id)
        chat_message = ChatMessage.objects.create(chat=chat, message=message)
        chat_message.save()
