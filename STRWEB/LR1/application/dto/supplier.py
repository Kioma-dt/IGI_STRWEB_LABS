from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.exceptions import BusinessValidationError


@dataclass(frozen=True)
class UpdateSupplyPriceDTO:
    product_id: UUID
    supplier_id: UUID
    new_purchase_price: Decimal

    def __post_init__(self) -> None:
        if self.new_purchase_price < 0:
            raise BusinessValidationError("Purchase price cannot be negative.")
