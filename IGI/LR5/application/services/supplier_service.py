from __future__ import annotations

import logging

from django.db import transaction

from application.dto.supplier import UpdateSupplyPriceDTO
from apps.suppliers.repositories.product_supplier_repository import (
    ProductSupplierRepository,
)

logger = logging.getLogger(__name__)


class SupplierService:
    """Supplier-side operations such as updating negotiated purchase prices."""

    def __init__(
        self,
        *,
        product_suppliers: ProductSupplierRepository | None = None,
    ) -> None:
        self._links = product_suppliers or ProductSupplierRepository()

    @transaction.atomic
    def update_supply_price(self, payload: UpdateSupplyPriceDTO) -> None:
        self._links.update_last_purchase_price(
            payload.product_id,
            payload.supplier_id,
            payload.new_purchase_price,
        )
        logger.info(
            "Updated supply price product=%s supplier=%s",
            payload.product_id,
            payload.supplier_id,
        )
