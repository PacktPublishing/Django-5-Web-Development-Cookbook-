from django.test import TestCase
from articles.models import Article
from articles.signals import article_pre_save
from django.db.models.signals import pre_save


class ArticlePreSaveTestCase(TestCase):
    def setUp(self):
        pre_save.connect(article_pre_save, sender=Article)

    def test_article_pre_save(self):
        article = Article(title="Test Article", description="Test Description")

        pre_save.send(sender=Article, instance=article)

        self.assertIsNotNone(article.slug)
        self.assertIsNotNone(article.updated)

    def tearDown(self):
        pre_save.connect(article_pre_save, sender=Article)
