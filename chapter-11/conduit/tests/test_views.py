import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from articles.models import Article
from tests.factories import ArticleFactory, UserFactory


@pytest.mark.django_db
def test_article_detail_view(client, user):
    article = ArticleFactory()
    response = client.get(reverse("article-detail-view", kwargs={"slug": article.slug}))
    assert response.status_code == 200
    assertTemplateUsed(response, "articles/article.html")
    assert response.context["article"] == article


@pytest.mark.django_db
def test_article_list_view(client, user):
    articles = ArticleFactory.create_batch(5)
    response = client.get(reverse("article-list"))
    assert response.status_code == 200
    assertTemplateUsed(response, "articles/home.html")
    assert len(response.context["articles"]) == 5
    assert all(article in response.context["articles"] for article in articles)


@pytest.mark.django_db
def test_article_update_view(client, user):
    client.force_login(user)
    article = ArticleFactory()
    image = SimpleUploadedFile(
        "test_image.jpg", b"file_content", content_type="image/jpeg"
    )
    response = client.post(
        reverse("create-article-view"),
        {
            "title": "New Article",
            "content": "New Content",
            "image": image,
            "author": article.author,
        },
    )
    assert response.status_code == 200
    assert Article.objects.count() == 1
    assertTemplateUsed(response, "articles/article_form.html")
