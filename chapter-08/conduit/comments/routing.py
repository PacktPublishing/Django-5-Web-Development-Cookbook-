# routing.py

from django.urls import path

from .consumers import CommentConsumer

websocket_urlpatterns = [
    path("ws/articles/<int:article_id>", CommentConsumer.as_asgi()),
]

print("websocket_urlpatterns:", websocket_urlpatterns)
