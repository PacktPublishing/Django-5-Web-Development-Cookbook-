import pytest
from rest_framework.test import APIClient
from factories import UserFactory, ArticleFactory
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return UserFactory()


@pytest.fixture
def test_article(test_user):
    return ArticleFactory(author=test_user)


# Test for creating an article
@pytest.mark.django_db
def test_create_article(api_client, test_user):
    api_client.force_authenticate(user=test_user)  # Authenticate user
    url = "/api/articles"
    article_data = {
        "article": {
            "title": "New Integration",
            "description": "This is a description",
            "body": "Content of the article",
            "metadata": {},
            # "tagList": ["tag1", "tag2"]
        }
    }
    response = api_client.post(url, article_data, format="json")

    # Debug log to check response
    logger.debug(f"Response Data: {response.data}")
    res_json = response.json()
    # Validate the response
    assert response.status_code == 201
    assert res_json["article"]["title"] == "New Integration"
    assert res_json["article"]["description"] == "This is a description"


# Test for listing articles
@pytest.mark.django_db
def test_list_articles(api_client, test_article):
    logger.debug("Test article: %s", test_article)
    url = "/api/articles"
    response = api_client.get(url, format="json")
    logger.debug("Response: %s", response)
    res = response.json()

    logger.debug("Response json: %s", res)

    # Debug log to check response data
    logger.debug("Response: %s", res)

    # Validate the response
    assert response.status_code == 200
    assert len(res) == 1
    assert res[0]["title"] == test_article.title


# Test for retrieving a specific article by slug
@pytest.mark.django_db
def test_retrieve_article(api_client, test_article):
    api_client.force_authenticate(
        user=test_article.author
    )  # Authenticate article author
    url = f"/api/articles/{test_article.slug}"
    response = api_client.get(url, format="json")
    response_data = response.json()

    # Debug log to check response
    logger.debug(f"Response: {response.data}")

    # Validate the response
    assert response.status_code == 200
    assert response_data["article"]["title"] == test_article.title


# Test for updating an article
@pytest.mark.django_db
def test_update_article(api_client, test_article):
    api_client.force_authenticate(
        user=test_article.author
    )  # Authenticate article author
    url = f"/api/articles/{test_article.slug}"
    updated_data = {
        "article": {
            "title": "Updated Title",
            "description": "Updated description",
            "body": "Updated body",
            "metadata": {},
        }
    }
    response = api_client.put(url, updated_data, format="json")
    response_data = response.json()

    logger.debug(f"Response: {response_data}")

    # Validate the response
    assert response.status_code == 200
    assert response_data["article"]["title"] == "Updated Title"


# Test for deleting an article
@pytest.mark.django_db
def test_delete_article(api_client, test_article):
    api_client.force_authenticate(
        user=test_article.author
    )  # Authenticate article author
    url = f"/api/articles/{test_article.slug}"
    response = api_client.delete(url, format="json")

    # Validate the response
    assert response.status_code == 204
