from django.test import TestCase
from django.utils import timezone

from apps.news.models import NewsArticle


class NewsArticleModelTest(TestCase):
    """Тесты для модели NewsArticle"""

    def test_create_news_article(self):
        article = NewsArticle.objects.create(
            title="Breaking News",
            slug="breaking-news",
            body="This is news content",
            is_published=True,
            published_at=timezone.now(),
        )
        self.assertEqual(str(article), "Breaking News")
        self.assertTrue(article.is_published)

    def test_news_article_unpublished(self):
        article = NewsArticle.objects.create(
            title="Draft",
            slug="draft",
            body="Draft content",
            is_published=False,
        )
        self.assertFalse(article.is_published)
        self.assertIsNone(article.published_at)

    def test_news_article_unique_slug(self):
        NewsArticle.objects.create(
            title="News1", slug="news", body="Content1", is_published=True
        )
        with self.assertRaises(Exception):
            NewsArticle.objects.create(
                title="News2", slug="news", body="Content2", is_published=True
            )

    def test_news_article_soft_delete(self):
        article = NewsArticle.objects.create(
            title="News", slug="news", body="Content", is_published=True
        )
        article.soft_delete()
        self.assertTrue(article.is_deleted)

    def test_news_article_ordering(self):
        now = timezone.now()
        article1 = NewsArticle.objects.create(
            title="Old", slug="old", body="Old", is_published=True, published_at=now
        )
        article2 = NewsArticle.objects.create(
            title="New",
            slug="new",
            body="New",
            is_published=True,
            published_at=now + timezone.timedelta(hours=1),
        )
        articles = list(
            NewsArticle.objects.filter(is_deleted=False, is_published=True)
        )
        self.assertEqual(articles[0].title, "New")  # Newest first
