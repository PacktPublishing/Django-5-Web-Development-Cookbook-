# comments/consumers.py

import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import (
    WebsocketConsumer,
)

logger = logging.getLogger(__name__)


class CommentConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article_id = None
        self.group_name = None

    def connect(self):
        self.article_id = self.scope["url_route"]["kwargs"]["article_id"]
        self.group_name = f"comments_{self.article_id}"
        logger.info(f"Connected to {self.group_name}")
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        logger.info("Disconnected")
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_name
        )
