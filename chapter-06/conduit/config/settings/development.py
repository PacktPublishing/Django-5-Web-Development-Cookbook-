"""
Django settings for conduit project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", default="conduit"),
        "USER": os.getenv("POSTGRES_USER", default="conduit"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="conduit"),
        "HOST": os.getenv("POSTGRES_DEFAULT_SERVER", default="localhost"),
        "PORT": os.getenv("POSTGRES_DEFAULT_PORT", default="5432"),
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.getenv("REDIS_SERVER", default="localhost"), 6379)],
        },
    },
}

ASGI_APPLICATION = "config.asgi.application"

# use default database router
DATABASE_ROUTERS = []
