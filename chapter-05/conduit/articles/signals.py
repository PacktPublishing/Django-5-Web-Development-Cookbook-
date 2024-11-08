import logging
from datetime import timezone

from core.utils import generate_random_string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import os

from .models import Article

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance: Article, **kwargs):
    if instance.avatar:
        os.chmod(instance.avatar.path, 0o644)

    MAXIMUM_SLUG_LENGTH = 255

    logger.info(f"pre_save called on {instance}")
    if instance and not instance.slug:
        slug = slugify(instance.title)

        unique = generate_random_string()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + "-" + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split("-")

            if len(parts) == 1:
                slug = slug[: MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        instance.slug = slug + "-" + unique
        instance.updated = timezone.now()
        logger.info("finished pre_save on {instance}")
