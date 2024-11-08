# Generated by Django 5.0.4 on 2024-05-13 04:32

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("title", models.CharField(max_length=150, unique=True)),
                ("summary", models.TextField(blank=True)),
                ("content", models.TextField(blank=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now_add=True)),
                ("status", models.CharField(max_length=10)),
                ("slug", models.SlugField(max_length=250, unique=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "favorites",
                    models.ManyToManyField(
                        related_name="favorites", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "tags",
                    taggit.managers.TaggableManager(
                        blank=True,
                        help_text="A comma-separated list of tags.",
                        through="taggit.TaggedItem",
                        to="taggit.Tag",
                        verbose_name="Tags",
                    ),
                ),
            ],
            options={
                "ordering": ["-created"],
                "indexes": [
                    models.Index(
                        fields=["-updated", "slug"], name="article_index"
                    )
                ],
            },
        ),
    ]