from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import TopicDetailConsamer, ChatConsumer, SearchChatConsamer
 
websocket_urlpatterns = [
    path('ws/topic_detail_questions/<int:pk>/', TopicDetailConsamer.as_asgi()),
    path('ws/question/<int:pk>/', ChatConsumer.as_asgi()),
    path('ws/search/<int:pk>/', SearchChatConsamer.as_asgi())
]