# tests/test_models.py
import pytest
from tests.factories import ArticleFactory, UserFactory


@pytest.mark.django_db
def test_create_article():
    article = ArticleFactory()

    assert article.title
    assert article.content
    assert article.author
    assert article.tags
    assert article.slug
    assert article.created_at
    assert article.updated_at


@pytest.mark.django_db
def test_create_author():
    author = UserFactory()

    assert author.name
    assert author.bio
    assert author.image
    assert author.linkedin_url
    assert author.followers
