from __future__ import annotations

from typing import Any
from uuid import UUID

from django.db import transaction

from apps.catalog.models import ProductStock
from core.repositories.django_model_repository import DjangoModelRepository


class ProductStockRepository(DjangoModelRepository[ProductStock]):
    """Persistence for product stock levels (ORM encapsulated here)."""

    def __init__(
        self,
        model: type[ProductStock] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            from django.apps import apps as django_apps

            model = django_apps.get_model("catalog", "ProductStock")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def get_for_product(
        self,
        product_id: UUID | str,
        *,
        for_update: bool = False,
    ) -> ProductStock | None:
        qs = self._alive_qs(self._qs()).filter(product_id=product_id)
        if for_update:
            qs = qs.select_for_update()
        return qs.select_related("product").first()

    def ensure_stock_row(
        self,
        product_id: UUID | str,
        initial_quantity: int = 0,
    ) -> ProductStock:
        with transaction.atomic():
            existing = self.get_for_product(product_id, for_update=True)
            if existing is not None:
                return existing
            return self.create(
                {
                    "product_id": product_id,
                    "quantity_on_hand": initial_quantity,
                },
            )

    def set_quantity(
        self,
        stock: ProductStock,
        new_quantity: int,
    ) -> ProductStock:
        stock.quantity_on_hand = new_quantity
        stock.save(update_fields=["quantity_on_hand", "updated_at"])
        return stock
