from __future__ import annotations

import logging
from typing import Any

from django.db import transaction
from django.db.models import Q, QuerySet

from apps.catalog.models import Category, Product
from apps.catalog.repositories.category_repository import CategoryRepository
from apps.catalog.repositories.product_repository import ProductRepository
from apps.catalog.repositories.product_stock_repository import ProductStockRepository
from apps.news.models import NewsArticle
from apps.news.repositories.news_article_repository import NewsArticleRepository
from apps.orders.models import Order
from apps.orders.repositories.order_repository import OrderRepository
from apps.promotions.models import PromoCode
from apps.promotions.repositories.promo_code_repository import PromoCodeRepository
from apps.reviews.models import Review
from apps.reviews.repositories.review_repository import ReviewRepository
from apps.suppliers.models import Supplier
from apps.suppliers.repositories.supplier_repository import SupplierRepository

logger = logging.getLogger(__name__)


def normalize_ordering(
    raw: str | None,
    allowed_fields: frozenset[str],
    *,
    default: str,
) -> str:
    if not raw or not isinstance(raw, str):
        return default
    raw = raw.strip()
    if not raw:
        return default
    desc = raw.startswith("-")
    field = raw[1:] if desc else raw
    if field not in allowed_fields:
        return default
    return f"-{field}" if desc else field


class ShopStaffCatalogService:
    CATEGORY_ORDER = frozenset({"name", "slug", "created_at", "updated_at"})
    PRODUCT_ORDER = frozenset(
        {"name", "sku", "base_price", "created_at", "updated_at", "is_active"},
    )

    def __init__(
        self,
        *,
        categories: CategoryRepository | None = None,
        products: ProductRepository | None = None,
        stocks: ProductStockRepository | None = None,
    ) -> None:
        self._categories = categories or CategoryRepository()
        self._products = products or ProductRepository()
        self._stocks = stocks or ProductStockRepository()

    def categories_base_queryset(self) -> QuerySet[Category]:
        return Category.objects.filter(is_deleted=False).select_related("parent")

    def category_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.CATEGORY_ORDER, default="-created_at")

    @transaction.atomic
    def persist_category(self, instance: Category) -> Category:
        instance.save()
        logger.info("Category saved id=%s", instance.pk)
        return instance

    def delete_category(self, instance: Category) -> None:
        self._categories.delete(instance)
        logger.info("Category soft-deleted id=%s", instance.pk)

    def products_base_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(is_deleted=False).select_related("category")

    def products_detail_queryset(self) -> QuerySet[Product]:
        return self.products_base_queryset().select_related("stock")

    def product_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.PRODUCT_ORDER, default="-created_at")

    @transaction.atomic
    def persist_new_product(self, instance: Product, *, initial_stock: int) -> Product:
        instance.save()
        self._stocks.ensure_stock_row(instance.pk, initial_quantity=max(0, int(initial_stock)))
        logger.info("Product created id=%s", instance.pk)
        return instance

    @transaction.atomic
    def persist_product_update(self, instance: Product) -> Product:
        instance.save()
        logger.info("Product updated id=%s", instance.pk)
        return instance

    def delete_product(self, instance: Product) -> None:
        self._products.delete(instance)
        logger.info("Product soft-deleted id=%s", instance.pk)


class ShopStaffSupplierService:
    SUPPLIER_ORDER = frozenset({"name", "is_active", "created_at", "updated_at"})

    def __init__(self, suppliers: SupplierRepository | None = None) -> None:
        self._suppliers = suppliers or SupplierRepository()

    def suppliers_base_queryset(self) -> QuerySet[Supplier]:
        return Supplier.objects.filter(is_deleted=False)

    def supplier_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.SUPPLIER_ORDER, default="-created_at")

    @transaction.atomic
    def persist_supplier(self, instance: Supplier) -> Supplier:
        instance.save()
        logger.info("Supplier saved id=%s", instance.pk)
        return instance

    def delete_supplier(self, instance: Supplier) -> None:
        self._suppliers.delete(instance)
        logger.info("Supplier soft-deleted id=%s", instance.pk)


class ShopStaffOrderService:
    ORDER_ORDER = frozenset(
        {
            "ordered_at",
            "status",
            "total_amount",
            "reference_number",
            "created_at",
            "updated_at",
        },
    )

    def __init__(self, orders: OrderRepository | None = None) -> None:
        self._orders = orders or OrderRepository()

    def orders_base_queryset(self) -> QuerySet[Order]:
        return Order.objects.filter(is_deleted=False).select_related(
            "customer",
            "created_by",
            "promo_code",
        )

    def orders_detail_queryset(self) -> QuerySet[Order]:
        from django.db.models import Prefetch

        from apps.orders.models import OrderItem

        return self.orders_base_queryset().prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.filter(is_deleted=False).select_related(
                    "product",
                ),
            ),
        )

    def order_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.ORDER_ORDER, default="-ordered_at")

    @transaction.atomic
    def persist_order(self, instance: Order) -> Order:
        instance.save()
        logger.info("Order saved id=%s", instance.pk)
        return instance

    @transaction.atomic
    def create_empty_order(self, instance: Order) -> Order:
        instance.total_amount = instance.total_amount or 0
        instance.save()
        logger.info("Order created id=%s", instance.pk)
        return instance

    def delete_order(self, instance: Order) -> None:
        self._orders.delete(instance)
        logger.info("Order soft-deleted id=%s", instance.pk)


class ShopStaffReviewService:
    REVIEW_ORDER = frozenset({"rating", "title", "created_at", "updated_at"})

    def __init__(self, reviews: ReviewRepository | None = None) -> None:
        self._reviews = reviews or ReviewRepository()

    def reviews_base_queryset(self) -> QuerySet[Review]:
        return Review.objects.filter(is_deleted=False).select_related("product", "customer")

    def review_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.REVIEW_ORDER, default="-created_at")

    @transaction.atomic
    def persist_review(self, instance: Review) -> Review:
        instance.save()
        logger.info("Review saved id=%s", instance.pk)
        return instance

    def delete_review(self, instance: Review) -> None:
        self._reviews.delete(instance)
        logger.info("Review soft-deleted id=%s", instance.pk)


class ShopStaffNewsService:
    NEWS_ORDER = frozenset(
        {"title", "slug", "published_at", "is_published", "created_at", "updated_at"},
    )

    def __init__(self, articles: NewsArticleRepository | None = None) -> None:
        self._articles = articles or NewsArticleRepository()

    def news_base_queryset(self) -> QuerySet[NewsArticle]:
        return NewsArticle.objects.filter(is_deleted=False)

    def news_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.NEWS_ORDER, default="-published_at")

    @transaction.atomic
    def persist_article(self, instance: NewsArticle) -> NewsArticle:
        instance.save()
        logger.info("News article saved id=%s", instance.pk)
        return instance

    def delete_article(self, instance: NewsArticle) -> None:
        self._articles.delete(instance)
        logger.info("News article soft-deleted id=%s", instance.pk)


class ShopStaffPromoService:
    PROMO_ORDER = frozenset(
        {
            "code",
            "discount_percent",
            "valid_from",
            "valid_until",
            "is_active",
            "current_uses",
            "created_at",
            "updated_at",
        },
    )

    def __init__(self, promos: PromoCodeRepository | None = None) -> None:
        self._promos = promos or PromoCodeRepository()

    def promos_base_queryset(self) -> QuerySet[PromoCode]:
        return PromoCode.objects.filter(is_deleted=False).prefetch_related("customers")

    def promo_ordering(self, raw: str | None) -> str:
        return normalize_ordering(raw, self.PROMO_ORDER, default="-created_at")

    @transaction.atomic
    def persist_promo_from_form(self, form: Any) -> PromoCode:
        obj = form.save()
        logger.info("Promo saved from form id=%s", obj.pk)
        return obj

    @transaction.atomic
    def persist_promo(self, instance: PromoCode) -> PromoCode:
        instance.save()
        logger.info("Promo saved id=%s", instance.pk)
        return instance

    def delete_promo(self, instance: PromoCode) -> None:
        self._promos.delete(instance)
        logger.info("Promo soft-deleted id=%s", instance.pk)


def apply_icontains_q(
    qs: QuerySet[Any],
    value: str,
    *field_names: str,
) -> QuerySet[Any]:
    if not value or not value.strip():
        return qs
    q = Q()
    for name in field_names:
        q |= Q(**{f"{name}__icontains": value.strip()})
    return qs.filter(q)
