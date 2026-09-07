from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.exceptions import BusinessValidationError


@dataclass(frozen=True)
class ApplyPromoInputDTO:
    promo_code: str
    customer_id: UUID
    order_subtotal: Decimal

    def __post_init__(self) -> None:
        if self.order_subtotal < 0:
            raise BusinessValidationError("Order subtotal cannot be negative.")
        code = self.promo_code.strip()
        if not code:
            raise BusinessValidationError("Promo code must not be empty.")
        object.__setattr__(self, "promo_code", code)


@dataclass(frozen=True)
class PromoDiscountResultDTO:
    promo_id: UUID | None
    promo_code: str | None
    discount_amount: Decimal
    discount_percent: Decimal
