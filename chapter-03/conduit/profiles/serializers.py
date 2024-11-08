from profiles.models import User
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "email", "password", "bio", "image")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        logger.info(f" # UPDATE : bio: {instance.bio}, image: {instance.image}")
        logger.info(f"instance: {instance}, validated_data: {validated_data}")

        for key, value in validated_data.items():
            logger.info(f"key: {key}, value: {value}")
            if key == "password":
                instance.set_password(value)
            elif key == "bio":  # Add this line to handle the 'bio' field
                setattr(instance, key, value)
            else:
                setattr(instance, key, value)
        logger.info(f" # after bio: {instance.bio}, image: {instance.image}")

        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("name", "bio", "image", "following")

    def get_following(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return obj.followers.filter(pk=request.user.id).exists()
