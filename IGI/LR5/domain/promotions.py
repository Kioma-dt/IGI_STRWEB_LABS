from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class PromoCode:
    id: UUID
    code: str
    discount_percent: Decimal
    valid_from: date
    valid_until: date | None
    max_uses: int | None
    current_uses: int
    is_active: bool
