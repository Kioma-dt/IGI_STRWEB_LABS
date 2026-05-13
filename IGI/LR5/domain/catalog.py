from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ProductStock:
    id: UUID
    product_id: UUID
    quantity_on_hand: int


@dataclass(frozen=True)
class Category:
    id: UUID
    name: str
    slug: str
    parent_id: UUID | None


@dataclass(frozen=True)
class Product:
    id: UUID
    name: str
    sku: str
    category_id: UUID | None
    base_price: Decimal
    age_restriction: int
    is_active: bool


@dataclass(frozen=True)
class Supplier:
    id: UUID
    name: str
    phone: str
    email: str
    is_active: bool


@dataclass(frozen=True)
class ProductSupplierLink:
    id: UUID
    product_id: UUID
    supplier_id: UUID
    last_purchase_price: Decimal
