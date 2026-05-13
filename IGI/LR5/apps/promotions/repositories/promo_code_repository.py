from __future__ import annotations

from datetime import date
from typing import Any, Mapping
from uuid import UUID

from django.apps import apps as django_apps
from django.utils import timezone

from apps.promotions.models import PromoCode
from core.repositories.django_model_repository import DjangoModelRepository
from core.repositories.pagination import RepositoryPage, paginate_queryset


def _get_model(app_label: str, model_name: str) -> type[Any]:
    return django_apps.get_model(app_label, model_name)


class PromoCodeRepository(DjangoModelRepository[PromoCode]):
    _ALLOWED_ORDERING_FIELDS = frozenset(
        {"created_at", "updated_at", "code", "discount_percent"},
    )

    def __init__(
        self,
        model: type[PromoCode] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            model = _get_model("promotions", "PromoCode")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def _validate_ordering(self, ordering: str) -> str:
        ordering = ordering.strip()
        if not ordering:
            return "-created_at"
        field = ordering[1:] if ordering.startswith("-") else ordering
        if field not in self._ALLOWED_ORDERING_FIELDS:
            raise ValueError(f"Unsupported ordering field: {field}")
        return ordering

    def get_by_id(self, entity_id: UUID | str) -> PromoCode | None:
        qs = self._alive_qs(self._qs()).prefetch_related("customers")
        return qs.filter(pk=entity_id).first()

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
        filters: Mapping[str, Any] | None = None,
        select_related: list[str] | None = None,
        prefetch_related: list[str] | None = None,
    ) -> RepositoryPage[PromoCode]:
        ordering = self._validate_ordering(ordering)
        pr = prefetch_related if prefetch_related is not None else ["customers"]
        return super().list(
            page=page,
            page_size=page_size,
            ordering=ordering,
            filters=filters,
            select_related=select_related or [],
            prefetch_related=pr,
        )

    def search(
        self,
        text: str,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
    ) -> RepositoryPage[PromoCode]:
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs()).prefetch_related("customers")
        qs = qs.search(text)
        return paginate_queryset(qs.order_by(ordering), page, page_size)

    def get_active_promocodes(
        self,
        on_date: date | None = None,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
    ) -> RepositoryPage[PromoCode]:
        if on_date is None:
            on_date = timezone.localdate()
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs()).prefetch_related("customers")
        qs = qs.active_on(on_date)
        return paginate_queryset(qs.order_by(ordering), page, page_size)
