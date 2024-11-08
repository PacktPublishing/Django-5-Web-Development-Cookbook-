# routing.py

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from .consumers import CommentConsumer

websocket_urlpatterns = [
    path("ws/articles/<int:article_id>", CommentConsumer.as_asgi()),
]

print("websocket_urlpatterns:", websocket_urlpatterns)
