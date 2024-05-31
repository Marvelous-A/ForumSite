from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import QuestionConsumer
 
websocket_urlpatterns = [
    path('ws/question/<int:pk>/', QuestionConsumer.as_asgi()),
]