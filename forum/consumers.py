from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import Message, User, Chat
from django.core.files.base import ContentFile
import base64
from django.utils import timezone

class SearchChatConsamer(AsyncWebsocketConsumer):
    async def connect(self):
        self.topic_id = self.scope['url_route']['kwargs']['pk']
        print(self.topic_id)
        self.room_group_name = f'topic_{self.topic_id}'
        print(self.room_group_name)

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
        print('вход')
        data_json = json.loads(text_data)
        print(data_json)
        
        if data_json.get('action') == 'delete':
            topic_id = data_json['id']
            # Удаление обсуждения из базы данных
            await self.delete_question(topic_id)
            # Отправка сообщения об удалении всем клиентам
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    'type': 'delete_question_message',
                    'id': topic_id,
                    'action': 'delete'
                }
            )

class TopicDetailConsamer(AsyncWebsocketConsumer):
    async def connect(self):
        self.topic_id = self.scope['url_route']['kwargs']['pk']
        print(self.topic_id)
        self.room_group_name = f'topic_{self.topic_id}'
        print(self.room_group_name)

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
        print('вход')
        data_json = json.loads(text_data)
        print(data_json)
        
        if data_json.get('action') == 'delete':
            topic_id = data_json['id']
            # Удаление обсуждения из базы данных
            await self.delete_question(topic_id)
            # Отправка сообщения об удалении всем клиентам
            await self.channel_layer.group_send(
                self.room_group_name, 
                {
                    'type': 'delete_question_message',
                    'id': topic_id,
                    'action': 'delete'
                }
            )


    async def delete_question_message(self, event):
        topic_id = event['id']

        # Отправка данных об удалении клиентам
        await self.send(text_data=json.dumps({
            'action': 'delete',
            'id': topic_id,
        }))

    @database_sync_to_async
    def delete_question(self, id, user, users_admin):
        try: 
            chat = Chat.objects.get(pk=id)
            if user == chat.author.username or user in users_admin:
                chat.delete()
        except Chat.DoesNotExist:
            print("Чат удалён")

class ChatConsumer(AsyncWebsocketConsumer):
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
        
        if "id" in text_data_json:
            message_id = text_data_json['id']
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
            if message_text == '':
                return
            image_data = text_data_json.get('image')
            message = await self.create_message(message_text, image_data)
            local_datetime = timezone.localtime(message.time)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_message',
                    'message': message_text,
                    'id': message.id,
                    'author': message.author.username,
                    'time': local_datetime.strftime("%H:%M")
                    }
                )
    
    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            "id": event['id'],
            "message": event['message'],
            "author": event['author'],
            "time": event['time']
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

    @database_sync_to_async
    def create_message(self, text, image_data=None):
        user = User.objects.get(username=self.scope["user"].username)
        question = Chat.objects.get(pk=self.question_id)
        message = Message(
            author=user,
            question=question,
            text=text
            )
        
        message.save()
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=f'message_{message.pk}.{ext}')
            message.image.save(f'message_image_{message.pk}.{ext}', image_file, save=True)
        return message