from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.exceptions import BusinessValidationError


@dataclass(frozen=True)
class SetBasePriceDTO:
    product_id: UUID
    new_price: Decimal

    def __post_init__(self) -> None:
        if self.new_price < 0:
            raise BusinessValidationError("Price cannot be negative.")


@dataclass(frozen=True)
class RestockProductDTO:
    product_id: UUID
    quantity_delta: int

    def __post_init__(self) -> None:
        if self.quantity_delta == 0:
            raise BusinessValidationError("quantity_delta must be non-zero.")


@dataclass(frozen=True)
class StockCheckResultDTO:
    product_id: UUID
    available: int
    requested: int
    sufficient: bool
