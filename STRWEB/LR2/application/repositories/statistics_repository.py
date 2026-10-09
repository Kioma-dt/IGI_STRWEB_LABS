from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Sum

from application.dto.statistics import ShopStatisticsDTO
from apps.catalog.models import Product, ProductStock
from apps.orders.models import Order
from apps.reviews.models import Review
from apps.suppliers.models import Supplier


@dataclass(frozen=True)
class StatisticsRepository:
    """
    Read-side persistence for dashboard aggregates.

    Keeps raw ORM aggregation out of services while remaining persistence-focused.
    """

    low_stock_threshold: int = 5

    def fetch_shop_statistics(self) -> ShopStatisticsDTO:
        revenue_agg = (
            Order.objects.filter(
                is_deleted=False,
                status__in=[
                    Order.Status.PAID,
                    Order.Status.COMPLETED,
                    Order.Status.SHIPPED,
                ],
            ).aggregate(s=Sum("total_amount"))
        )
        revenue = revenue_agg["s"] or Decimal("0.00")

        orders_total = Order.objects.filter(is_deleted=False).count()

        active_products = Product.objects.filter(
            is_deleted=False,
            is_active=True,
        ).count()

        published_reviews = Review.objects.filter(
            is_deleted=False,
            is_published=True,
        ).count()

        low_stock = (
            ProductStock.objects.filter(
                is_deleted=False,
                quantity_on_hand__lt=self.low_stock_threshold,
            ).count()
        )

        active_suppliers = Supplier.objects.filter(
            is_deleted=False,
            is_active=True,
        ).count()

        return ShopStatisticsDTO(
            orders_total_count=orders_total,
            orders_revenue=revenue,
            active_products_count=active_products,
            published_reviews_count=published_reviews,
            low_stock_product_count=low_stock,
            active_suppliers_count=active_suppliers,
        )
