from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.exceptions import BusinessValidationError


@dataclass(frozen=True)
class OrderLineInputDTO:
    product_id: UUID
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity < 1:
            raise BusinessValidationError("Order line quantity must be at least 1.")


@dataclass(frozen=True)
class PlaceOrderDTO:
    customer_id: UUID
    lines: tuple[OrderLineInputDTO, ...]
    promo_code: str | None = None
    created_by_employee_id: UUID | None = None

    def __post_init__(self) -> None:
        if not self.lines:
            raise BusinessValidationError("Order must contain at least one line.")
        if self.promo_code is not None:
            normalized = self.promo_code.strip()
            object.__setattr__(self, "promo_code", normalized or None)


@dataclass(frozen=True)
class OrderPlacedResultDTO:
    order_id: UUID
    reference_number: str
    subtotal: Decimal
    discount: Decimal
    total: Decimal
    promo_code: str | None


@dataclass(frozen=True)
class OrderTotalsPreviewDTO:
    """Read-model for calculated totals (no persistence)."""

    subtotal: Decimal
    discount: Decimal
    total: Decimal
    currency: str = "BYN"
