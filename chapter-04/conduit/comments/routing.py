# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from .consumers import CommentConsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path("ws/articles/<int:article_id>", CommentConsumer.as_asgi()),
]

print("websocket_urlpatterns:", websocket_urlpatterns)
