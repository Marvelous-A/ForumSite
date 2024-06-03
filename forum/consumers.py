from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message, User, Question

class QuestionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.question_id = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = f'question_{self.question_id}'

        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
            )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_id = text_data_json['id']
        
        if "id" in text_data_json:
            # Удаление сообщения из базы данных
            await self.delete_message(message_id)
            # Отправка сообщения об удалении всем клиентам
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    'type': 'question_message',
                    'id': message_id,
                }
            )
        
        if 'text' in text_data_json:
            message_text = text_data_json['text']
            message = self.create_message(message_text)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'message': message_text,
                    'id': message.id,
                    'author': message.author.username
                    }
                )
    
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "id": event['id'],
            "message": event['message'],
            "author": event['author']
            })
        )

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
            message = Message.objects.get(pk=id)
            message.delete()
        except Message.DoesNotExist:
            print("Сообщения не существует")
    
    def create_message(self, text):
        user = User.objects.get(username=self.scope["user"].username)
        question = Question.objects.get(pk=self.question_id)

        message = Message.objects.create(
            author=user,
            question=question,
            text=text
            )
        return message