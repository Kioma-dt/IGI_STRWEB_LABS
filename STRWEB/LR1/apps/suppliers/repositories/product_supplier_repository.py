from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.suppliers.models import ProductSupplier
from core.repositories.django_model_repository import DjangoModelRepository


class ProductSupplierRepository(DjangoModelRepository[ProductSupplier]):
    def __init__(
        self,
        model: type[ProductSupplier] | None = None,
        queryset_factory: Any | None = None,
    ) -> None:
        if model is None:
            from django.apps import apps as django_apps

            model = django_apps.get_model("suppliers", "ProductSupplier")
        super().__init__(model=model, queryset_factory=queryset_factory)

    def get_link(
        self,
        product_id: UUID | str,
        supplier_id: UUID | str,
        *,
        for_update: bool = False,
    ) -> ProductSupplier | None:
        qs = self._alive_qs(self._qs()).filter(
            product_id=product_id,
            supplier_id=supplier_id,
        )
        if for_update:
            qs = qs.select_for_update()
        return qs.first()

    def update_last_purchase_price(
        self,
        product_id: UUID | str,
        supplier_id: UUID | str,
        new_price: Decimal,
    ) -> ProductSupplier:
        with transaction.atomic():
            link = self.get_link(product_id, supplier_id, for_update=True)
            if link is None:
                from core.exceptions import ProductSupplierLinkNotFoundError

                raise ProductSupplierLinkNotFoundError(
                    "No supplier link exists for this product and supplier.",
                )
            link.last_purchase_price = new_price
            link.save(update_fields=["last_purchase_price", "updated_at"])
            return link
