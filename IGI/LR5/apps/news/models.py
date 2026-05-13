from __future__ import annotations

from django.db import models

from apps.news.managers import NewsArticleManager
from core.models import SoftDeleteModel


class NewsArticle(SoftDeleteModel):
    title = models.CharField("title", max_length=255)
    slug = models.SlugField("slug", max_length=255, unique=True)
    body = models.TextField("body")
    published_at = models.DateTimeField(
        "published at",
        null=True,
        blank=True,
        db_index=True,
    )
    is_published = models.BooleanField("published", default=False)

    objects = NewsArticleManager()

    class Meta:
        verbose_name = "news article"
        verbose_name_plural = "news articles"
        indexes = [
            models.Index(fields=["is_published"], name="news_published_idx"),
        ]

    def __str__(self) -> str:
        return self.title
