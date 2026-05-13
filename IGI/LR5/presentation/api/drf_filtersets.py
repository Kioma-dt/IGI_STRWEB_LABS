from __future__ import annotations

import django_filters
from django.db.models import Q

from apps.catalog.models import Category, Product
from apps.news.models import NewsArticle
from apps.orders.models import Order
from apps.promotions.models import PromoCode
from apps.reviews.models import Review


class CategoryAPIFilter(django_filters.FilterSet):
    parent = django_filters.UUIDFilter(field_name="parent_id")
    name = django_filters.CharFilter(lookup_expr="icontains")
    slug = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields: tuple[str, ...] = ("parent",)


class ProductAPIFilter(django_filters.FilterSet):
    category = django_filters.UUIDFilter(field_name="category_id")
    is_active = django_filters.BooleanFilter()
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ("category", "is_active")


class OrderAPIFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    customer = django_filters.UUIDFilter(field_name="customer_id")
    ordered_at_after = django_filters.IsoDateTimeFilter(field_name="ordered_at", lookup_expr="gte")
    ordered_at_before = django_filters.IsoDateTimeFilter(field_name="ordered_at", lookup_expr="lte")

    class Meta:
        model = Order
        fields = ("status", "customer")


class ReviewAPIFilter(django_filters.FilterSet):
    product = django_filters.UUIDFilter(field_name="product_id")
    customer = django_filters.UUIDFilter(field_name="customer_id")
    is_published = django_filters.BooleanFilter()
    rating = django_filters.NumberFilter()

    class Meta:
        model = Review
        fields = ("product", "customer", "is_published", "rating")


class NewsArticleAPIFilter(django_filters.FilterSet):
    is_published = django_filters.BooleanFilter()
    slug = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = NewsArticle
        fields = ("is_published",)


class PromoCodeAPIFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter()
    code = django_filters.CharFilter(lookup_expr="icontains")
    valid_on = django_filters.DateFilter(method="filter_valid_on")

    class Meta:
        model = PromoCode
        fields = ("is_active",)

    def filter_valid_on(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            Q(valid_from__lte=value) & (Q(valid_until__gte=value) | Q(valid_until__isnull=True)),
        )
