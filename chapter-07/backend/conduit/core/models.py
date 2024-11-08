import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class SoftDeletableModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        logger.info(f"delete called on {self}")
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()

    def restore(self):
        self.deleted_at = None
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def is_deleted(self):
        return self.deleted_at is not None
