import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Article

logger = logging.getLogger(__name__)

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "name",
            "bio",
            "image",
            "following",
        )

    def get_following(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.followers.filter(pk=user.pk).exists()
        return False


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    author = AuthorSerializer(read_only=True)
    description = serializers.CharField(source="summary")
    body = serializers.CharField(source="content")
    tagList = TagListSerializerField(source="tags", required=False)
    createdAt = serializers.DateTimeField(
        source="created", format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    updatedAt = serializers.DateTimeField(
        source="updated", format="%Y-%m-%dT%H:%M:%S.%fZ", required=False
    )
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()

    metadata = serializers.JSONField()  # Add this line

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "description",
            "body",
            "image",
            "tagList",
            "createdAt",
            "updatedAt",
            "favorited",
            "favoritesCount",
            "author",
            "metadata",
        )
        reaad_only_fields = ("slug", "createdAt", "updatedAt", "author")

    def get_author(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return None
        author = AuthorSerializer(
            obj.author, context={"request": request}
        ).data
        logger.info(f"author: {author}")
        return author

    def get_favorited(self, obj):

        request = self.context.get("request", None)
        if request is None:
            return False
        user = request.user
        logger.info(f" get_favorited user: {user}, obj: {obj}")
        if user.is_authenticated and hasattr(obj, "favorites"):
            return obj.favorites.filter(pk=user.pk).exists()
        return False

    def get_favoritesCount(self, obj):
        if not hasattr(obj, "favorites"):
            return 0
        return obj.favorites.count()

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        article = Article.objects.create(
            author=self.context["request"].user, **validated_data
        )

        article.tags.add(*tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", [])
        instance.tags.add(*tags)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class TagSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField())
