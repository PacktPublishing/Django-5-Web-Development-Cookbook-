import pytest
from tests.factories import ArticleFactory, UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def articles():
    return ArticleFactory.create_batch(5)


# patch the article_pre_save signal handler
@pytest.fixture
def patch_article_pre_save_signal_handler(mocker):
    return mocker.patch("articles.signals.article_pre_save_handler")
