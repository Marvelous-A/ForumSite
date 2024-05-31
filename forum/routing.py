from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import QuestionConsumer
 
websocket_urlpatterns = [
    path('ws/question/', QuestionConsumer.as_asgi()),
]