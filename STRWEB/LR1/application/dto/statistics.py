from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ShopStatisticsDTO:
    orders_total_count: int
    orders_revenue: Decimal
    active_products_count: int
    published_reviews_count: int
    low_stock_product_count: int
    active_suppliers_count: int
