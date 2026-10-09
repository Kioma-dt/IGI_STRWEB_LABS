from __future__ import annotations

from django.db import models

from apps.news.querysets import NewsArticleQuerySet


class NewsArticleManager(models.Manager["NewsArticle"]):
    def get_queryset(self) -> NewsArticleQuerySet:
        return NewsArticleQuerySet(self.model, using=self._db)
