from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class Purchase:
    id: UUID
    supplier_id: UUID
    created_by_employee_id: UUID | None
    ordered_at: datetime
    delivered_at: datetime | None
    reference_number: str


@dataclass(frozen=True)
class PurchaseItem:
    id: UUID
    purchase_id: UUID
    product_id: UUID
    quantity: int
    purchase_price: Decimal


@dataclass(frozen=True)
class Order:
    id: UUID
    customer_id: UUID | None
    created_by_employee_id: UUID | None
    promo_code_id: UUID | None
    status: str
    ordered_at: datetime
    total_amount: Decimal
    reference_number: str


@dataclass(frozen=True)
class OrderItem:
    id: UUID
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    line_total: Decimal
