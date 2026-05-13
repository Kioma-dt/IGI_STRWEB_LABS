from __future__ import annotations

import django_filters
from django.db.models import Q

from application.services.shop_staff_services import apply_icontains_q
from apps.catalog.models import Category, Product
from apps.news.models import NewsArticle
from apps.orders.models import Order
from apps.promotions.models import PromoCode
from apps.reviews.models import Review
from apps.suppliers.models import Supplier
from apps.users.models import CustomerProfile


class CategoryFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    name = django_filters.CharFilter(lookup_expr="icontains")
    slug = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Category
        fields = ("parent",)

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "name", "slug")


class ProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    name = django_filters.CharFilter(lookup_expr="icontains")
    sku = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_deleted=False),
        null_label="Any category",
    )
    min_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(field_name="base_price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ("name", "sku", "is_active", "category")

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "name", "sku")


class SupplierFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Supplier
        fields = ("is_active",)

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "name", "phone", "email")


class OrderFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    status = django_filters.ChoiceFilter(choices=Order.Status.choices)
    customer = django_filters.ModelChoiceFilter(
        queryset=CustomerProfile.objects.filter(is_deleted=False),
        null_label="Any customer",
    )

    class Meta:
        model = Order
        fields = ("status", "customer")

    def filter_q(self, queryset, name, value):
        v = (value or "").strip()
        if not v:
            return queryset
        return queryset.filter(
            Q(reference_number__icontains=v)
            | Q(status__icontains=v)
            | Q(customer__full_name__icontains=v),
        )


class ReviewFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.filter(is_deleted=False),
        null_label="Any product",
    )
    customer = django_filters.ModelChoiceFilter(
        queryset=CustomerProfile.objects.filter(is_deleted=False),
        null_label="Any customer",
    )
    is_published = django_filters.BooleanFilter()
    rating = django_filters.NumberFilter()

    class Meta:
        model = Review
        fields = ("product", "customer", "is_published", "rating")

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "title", "body")


class NewsArticleFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    is_published = django_filters.BooleanFilter()

    class Meta:
        model = NewsArticle
        fields = ("is_published",)

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "title", "slug", "body")


class PromoCodeFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q")
    code = django_filters.CharFilter(lookup_expr="icontains")
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = PromoCode
        fields = ("is_active",)

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "code")
