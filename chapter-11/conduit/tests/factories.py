from profile import Profile

import factory

# from django.forms import ImageField
from factory.django import ImageField

from articles.models import Article
from profiles.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    name = factory.Faker("name")
    password = factory.Faker("password")
    bio = factory.Faker("sentence")
    image = factory.django.ImageField(color="blue")
    is_active = factory.Faker("boolean")
    linkedin_url = factory.Faker("url")


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    summary = factory.Faker("sentence")
    author = factory.SubFactory(UserFactory)
    tags = factory.Faker("word")
    slug = factory.Faker("slug")
    created = factory.Faker("date_time")
    updated = factory.Faker("date_time")
    image = factory.django.ImageField(color="blue")
