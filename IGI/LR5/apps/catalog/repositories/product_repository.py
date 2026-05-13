from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping
from uuid import UUID

from django.apps import apps as django_apps

from apps.catalog.models import Category, Product
from core.exceptions import ProductNotFoundError
from core.repositories.django_model_repository import DjangoModelRepository
from core.repositories.pagination import RepositoryPage, paginate_queryset


def _get_model(app_label: str, model_name: str) -> type[Any]:
    return django_apps.get_model(app_label, model_name)


class ProductRepository(DjangoModelRepository[Product]):
    """
    Repository for Product aggregate roots.

    Encapsulates ORM access: optimized relations, sorting, filtering, search.
    """

    _ALLOWED_ORDERING_FIELDS = frozenset(
        {"created_at", "updated_at", "name", "base_price"},
    )

    def __init__(
        self,
        model: type[Product] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            model = _get_model("catalog", "Product")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def _validate_ordering(self, ordering: str) -> str:
        ordering = ordering.strip()
        if not ordering:
            return "-created_at"
        field = ordering[1:] if ordering.startswith("-") else ordering
        if field not in self._ALLOWED_ORDERING_FIELDS:
            raise ValueError(f"Unsupported ordering field: {field}")
        return ordering

    def get_by_id(self, entity_id: UUID | str) -> Product | None:
        qs = self._alive_qs(self._qs())
        qs = qs.select_related("category").prefetch_related("suppliers")
        return qs.filter(pk=entity_id).first()

    def list(
        self,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
        filters: Mapping[str, Any] | None = None,
        select_related: list[str] | None = None,
        prefetch_related: list[str] | None = None,
    ) -> RepositoryPage[Product]:
        ordering = self._validate_ordering(ordering)
        sr = select_related if select_related is not None else ["category"]
        pr = prefetch_related if prefetch_related is not None else ["suppliers"]
        return super().list(
            page=page,
            page_size=page_size,
            ordering=ordering,
            filters=filters,
            select_related=sr,
            prefetch_related=pr,
        )

    def search(
        self,
        text: str,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
    ) -> RepositoryPage[Product]:
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs())
        qs = qs.select_related("category").prefetch_related("suppliers")
        qs = qs.search(text)
        return paginate_queryset(qs.order_by(ordering), page, page_size)

    def filter_by_category(
        self,
        category_id: UUID | str,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
    ) -> RepositoryPage[Product]:
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs())
        qs = qs.select_related("category").prefetch_related("suppliers")
        qs = qs.filter_by_category(str(category_id))
        return paginate_queryset(qs.order_by(ordering), page, page_size)

    def filter_by_price(
        self,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
        page: int = 1,
        page_size: int = 20,
        ordering: str = "-created_at",
    ) -> RepositoryPage[Product]:
        ordering = self._validate_ordering(ordering)
        qs = self._alive_qs(self._qs())
        qs = qs.select_related("category").prefetch_related("suppliers")
        qs = qs.filter_by_price(min_price=min_price, max_price=max_price)
        return paginate_queryset(qs.order_by(ordering), page, page_size)

    def get_popular_products(self, limit: int = 10) -> list[Product]:
        qs = self._alive_qs(self._qs())
        qs = qs.select_related("category").prefetch_related("suppliers")
        popular_qs = qs.popular_products(limit=limit)
        return list(popular_qs)

    def lock_active_by_ids(self, ids: list[UUID]) -> dict[UUID, Product]:
        """Lock active products for update; used by transactional order placement."""
        if not ids:
            return {}
        unique_ids = list(dict.fromkeys(ids))
        rows = list(
            self._alive_qs(self._qs())
            .filter(id__in=unique_ids, is_active=True)
            .select_related("category")
            .select_for_update(),
        )
        found: dict[UUID, Product] = {p.id: p for p in rows}
        if len(found) != len(unique_ids):
            raise ProductNotFoundError(
                "One or more products are missing, inactive, or deleted.",
            )
        return found
