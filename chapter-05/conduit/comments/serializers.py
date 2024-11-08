import logging

from articles.serializers import AuthorSerializer
from comments.models import Comment
from rest_framework import serializers

logger = logging.getLogger(__name__)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(
        source="created", format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    updatedAt = serializers.DateTimeField(
        source="updated", format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    body = serializers.CharField(source="content", required=False)

    class Meta:
        model = Comment
        fields = ("id", "createdAt", "updatedAt", "body", "author")

    def get_author(self, obj):
        logger.debug(f"Getting author for comment: {obj}")
        request = self.context.get("request")
        serializer = AuthorSerializer(obj.author, context={"request": request})
        logger.debug(f"Author serializer: {serializer}")
        author = serializer.data
        logger.debug(f"Author: {author}")
        return author

    def create(self, validated_data):
        logger.debug(f"Creating comment with data: {validated_data}")
        logger.debug(f"Context: {self.context}")
        comment = Comment.objects.create(
            **validated_data,
            author=self.context.get("request").user,
            article=self.context.get("article"),
        )
        comment.save()
        return comment
