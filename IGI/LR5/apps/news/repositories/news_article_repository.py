from __future__ import annotations

from typing import Any, Mapping
from uuid import UUID

from django.apps import apps as django_apps

from apps.news.models import NewsArticle
from core.repositories.django_model_repository import DjangoModelRepository
from core.repositories.pagination import RepositoryPage, paginate_queryset


def _get_model(app_label: str, model_name: str) -> type[Any]:
    return django_apps.get_model(app_label, model_name)


class NewsArticleRepository(DjangoModelRepository[NewsArticle]):
    _ALLOWED_ORDERING_FIELDS = frozenset(
        {"created_at", "updated_at", "published_at", "title"},
    )

    def __init__(
        self,
        model: type[NewsArticle] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            model = _get_model("news", "NewsArticle")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def _validate_ordering(self, ordering: str) -> str:
        ordering = ordering.strip()
        if not ordering:
            return "-published_at"
        field = ordering[1:] if ordering.startswith("-") else ordering
        if field not in self._ALLOWED_ORDERING_FIELDS:
            raise ValueError(f"Unsupported ordering field: {field}")
        return ordering

    def get_by_id(self, entity_id: UUID | str) -> NewsArticle | None:
        return self._alive_qs(self._qs()).filter(pk=entity_id).first()

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-published_at",
        filters: Mapping[str, Any] | None = None,
        select_related: list[str] | None = None,
        prefetch_related: list[str] | None = None,
    ) -> RepositoryPage[NewsArticle]:
        ordering = self._validate_ordering(ordering)
        return super().list(
            page=page,
            page_size=page_size,
            ordering=ordering,
            filters=filters,
            select_related=select_related or [],
            prefetch_related=prefetch_related or [],
        )

    def search(
        self,
        text: str,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-published_at",
    ) -> RepositoryPage[NewsArticle]:
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs())
        qs = qs.search(text)
        return paginate_queryset(qs.order_by(ordering), page, page_size)

    def get_latest_news(self, limit: int = 10) -> list[NewsArticle]:
        qs = self._alive_qs(self._qs())
        latest_qs = qs.latest_news(limit=limit)
        return list(latest_qs)
