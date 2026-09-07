from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.news.models import NewsArticle


class NewsArticleQuerySet(SoftDeleteQuerySet["NewsArticle"]):
    def published(self) -> QuerySet["NewsArticle"]:
        return self.alive().filter(is_published=True)

    def search(self, text: str) -> QuerySet["NewsArticle"]:
        return self.published().filter(
            Q(title__icontains=text) | Q(slug__icontains=text),
        )

    def latest_news(self, limit: int = 10) -> QuerySet["NewsArticle"]:
        return (
            self.published()
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:limit]
        )
