from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import QuestionConsumer

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/questions/', QuestionConsumer.as_asgi()),
    ]),
})