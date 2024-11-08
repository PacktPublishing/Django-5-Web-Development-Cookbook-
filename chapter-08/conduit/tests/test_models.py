import pytest
from articles.models import Article
from profiles.models import User
from tests.factories import ArticleFactory


@pytest.mark.django_db
def test_article_creation():
    article = ArticleFactory()
    assert article.title is not None
    assert article.content is not None
    assert article.author is not None
    assert article.tags is not None
    assert article.slug is not None
    assert article.created_at is not None
    assert article.updated_at is not None


@pytest.mark.django_db  # Ensures that the test database is used
def test_create_user():
    user = User.objects.create_user(
        email="john@me.com", name="john", password="pass123"
    )
    assert user.name == "john"
    assert user.is_active  # Check that the user is active by default


@pytest.mark.django_db
def test_check_password():
    user = User.objects.create_user(
        email="john@me.com", name="john", password="pass123"
    )
    assert (
        user.check_password("pass123") is True
    )  # Test that the password is set correctly


@pytest.mark.django_db
def test_create_article():
    article_orm = ArticleFactory.build()
    author = User.objects.create_user(
        email=article_orm.author.email,
        name=article_orm.author.name,
        password="pass123",
    )
    author.save()
    article_orm = Article.objects.create(
        title=article_orm.title,
        content=article_orm.content,
        author=author,
        tags=article_orm.tags,
        slug=article_orm.slug,
        created_at=article_orm.created_at,
        updated_at=article_orm.updated_at,
    )
    article_orm.save()
    article = Article.objects.get(slug=article_orm.slug)
    assert article.title == article_orm.title
    assert article.content == article_orm.content
    assert article.author == author
    assert article.slug == article_orm.slug
    assert article.created_at == article_orm.created_at
    assert article.updated_at == article_orm.updated_at
