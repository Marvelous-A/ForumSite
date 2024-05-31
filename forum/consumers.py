from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Question

class QuestionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'question_room'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_id = text_data_json['id']

        # Удаление сообщения из базы данных
        await self.delete_message(message_id)

        # Отправка сообщения об удалении всем клиентам
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'question_message',
            'id': message_id,
        })

    async def question_message(self, event):
        message_id = event['id']

        # Отправка данных об удалении клиентам
        await self.send(text_data=json.dumps({
            'id': message_id,
        }))
        
    @database_sync_to_async
    def delete_message(self, id):
        # Здесь логика удаления сообщения из базы данных
        try: 
            Question.objects.get(pk=id).delete()
        except Question.DoesNotExist:
            pass