from articles.models import Article
from django.conf import settings
from django.db import models


class CommentQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status="approved")


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()


class Comment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
    ]

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CommentManager()
