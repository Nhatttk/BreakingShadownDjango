from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/private-chat/<int:chat_id>/', consumers.PrivateChatConsumer.as_asgi()),
]
