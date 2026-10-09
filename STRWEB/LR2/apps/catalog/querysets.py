from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from django.db.models import Avg, Count, DecimalField, Q, QuerySet, Value
from django.db.models.functions import Coalesce

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.catalog.models import Category, Product


class CategoryQuerySet(SoftDeleteQuerySet["Category"]):
    def active(self) -> QuerySet["Category"]:
        return self.alive()

    def search(self, text: str) -> QuerySet["Category"]:
        return self.active().filter(
            Q(name__icontains=text) | Q(slug__icontains=text),
        )


class ProductQuerySet(SoftDeleteQuerySet["Product"]):
    def active(self) -> QuerySet["Product"]:
        return self.alive().filter(is_active=True)

    def search(self, text: str) -> QuerySet["Product"]:
        return self.active().filter(
            Q(name__icontains=text) | Q(sku__icontains=text),
        )

    def filter_by_category(self, category_id: str) -> QuerySet["Product"]:
        return self.active().filter(category_id=category_id)

    def filter_by_price(
        self,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> QuerySet["Product"]:
        qs = self.active()
        if min_price is not None:
            qs = qs.filter(base_price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(base_price__lte=max_price)
        return qs

    def popular_products(self, limit: int = 10) -> QuerySet["Product"]:
        published = Q(
            reviews__is_deleted=False,
            reviews__is_published=True,
        )
        qs = self.active().annotate(
            avg_rating=Coalesce(
                Avg("reviews__rating", filter=published),
                Value(Decimal("0.00"), output_field=DecimalField(max_digits=6, decimal_places=2)),
                output_field=DecimalField(max_digits=6, decimal_places=2),
            ),
            reviews_count=Count("reviews", filter=published),
        )
        return qs.order_by("-reviews_count", "-avg_rating")[:limit]
