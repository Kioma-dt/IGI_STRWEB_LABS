from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db.models import Sum

from apps.orders.models import OrderItem
from core.repositories.django_model_repository import DjangoModelRepository


class OrderItemRepository(DjangoModelRepository[OrderItem]):
    def __init__(
        self,
        model: type[OrderItem] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            from django.apps import apps as django_apps

            model = django_apps.get_model("orders", "OrderItem")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def bulk_create_items(self, items: list[OrderItem]) -> list[OrderItem]:
        return self._model.objects.bulk_create(items)

    def sum_quantity_for_product(self, product_id: UUID | str) -> int:
        agg = (
            self._alive_qs(self._qs())
            .filter(product_id=product_id)
            .aggregate(total=Sum("quantity"))
        )
        return int(agg["total"] or 0)
