from __future__ import annotations

from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle

from django_filters.rest_framework import DjangoFilterBackend

from apps.catalog.models import Category, Product
from apps.news.models import NewsArticle
from apps.orders.models import Order, OrderItem
from apps.promotions.models import PromoCode
from apps.reviews.models import Review
from apps.users.permissions import django_permission
from presentation.api.drf_filtersets import (
    CategoryAPIFilter,
    NewsArticleAPIFilter,
    OrderAPIFilter,
    ProductAPIFilter,
    PromoCodeAPIFilter,
    ReviewAPIFilter,
)
from presentation.api.pagination import ZoomShopPageNumberPagination
from presentation.api.permissions import CatalogEditorOrReadOnly, NewsPromoEditorOrReadOnly
from presentation.api.serializers import (
    CategorySerializer,
    NewsArticleSerializer,
    OrderSerializer,
    ProductSerializer,
    PromoCodeSerializer,
    ReviewSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List categories", tags=["Categories"]),
    retrieve=extend_schema(summary="Retrieve category", tags=["Categories"]),
    create=extend_schema(summary="Create category", tags=["Categories"]),
    update=extend_schema(summary="Update category", tags=["Categories"]),
    partial_update=extend_schema(summary="Partially update category", tags=["Categories"]),
    destroy=extend_schema(summary="Delete category", tags=["Categories"]),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_deleted=False).select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = [CatalogEditorOrReadOnly]
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CategoryAPIFilter
    search_fields = ("name", "slug", "description")
    ordering_fields = ("name", "slug", "created_at", "updated_at")
    ordering = ("-created_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "categories"


@extend_schema_view(
    list=extend_schema(summary="List products", tags=["Products"]),
    retrieve=extend_schema(summary="Retrieve product", tags=["Products"]),
    create=extend_schema(summary="Create product", tags=["Products"]),
    update=extend_schema(summary="Update product", tags=["Products"]),
    partial_update=extend_schema(summary="Partially update product", tags=["Products"]),
    destroy=extend_schema(summary="Delete product", tags=["Products"]),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).select_related("category", "stock")
    serializer_class = ProductSerializer
    permission_classes = [CatalogEditorOrReadOnly]
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductAPIFilter
    search_fields = ("name", "sku", "description")
    ordering_fields = ("name", "sku", "base_price", "is_active", "created_at", "updated_at")
    ordering = ("-created_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "products"


@extend_schema_view(
    list=extend_schema(summary="List orders", tags=["Orders"]),
    retrieve=extend_schema(summary="Retrieve order", tags=["Orders"]),
    create=extend_schema(summary="Create order", tags=["Orders"]),
    update=extend_schema(summary="Update order", tags=["Orders"]),
    partial_update=extend_schema(summary="Partially update order", tags=["Orders"]),
    destroy=extend_schema(summary="Delete order", tags=["Orders"]),
)
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderAPIFilter
    search_fields = ("reference_number", "status", "customer__full_name")
    ordering_fields = ("ordered_at", "status", "total_amount", "reference_number", "created_at")
    ordering = ("-ordered_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "orders"

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated(), django_permission("users.view_sales")()]
        return [IsAuthenticated(), django_permission("users.full_access")()]

    def get_queryset(self):
        qs = Order.objects.filter(is_deleted=False).select_related(
            "customer",
            "created_by",
            "promo_code",
        )
        return qs.prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.filter(is_deleted=False).select_related("product"),
            ),
        )

    def perform_create(self, serializer) -> None:
        serializer.save()


@extend_schema_view(
    list=extend_schema(summary="List reviews", tags=["Reviews"]),
    retrieve=extend_schema(summary="Retrieve review", tags=["Reviews"]),
    create=extend_schema(summary="Create review", tags=["Reviews"]),
    update=extend_schema(summary="Update review", tags=["Reviews"]),
    partial_update=extend_schema(summary="Partially update review", tags=["Reviews"]),
    destroy=extend_schema(summary="Delete review", tags=["Reviews"]),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReviewAPIFilter
    search_fields = ("title", "body")
    ordering_fields = ("rating", "title", "created_at", "updated_at")
    ordering = ("-created_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "reviews"

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action == "create":
            return [IsAuthenticated(), django_permission("users.submit_product_review")()]
        return [IsAuthenticated(), django_permission("users.full_access")()]

    def get_queryset(self):
        qs = Review.objects.filter(is_deleted=False).select_related("product", "customer")
        u = self.request.user
        if not u.is_authenticated or not (u.is_staff or u.is_superuser):
            qs = qs.filter(is_published=True)
        return qs

    def perform_create(self, serializer) -> None:
        u = self.request.user
        if u.is_staff or u.is_superuser or u.has_perm("users.full_access"):
            serializer.save()
            return
        profile = getattr(u, "customer_profile", None)
        if profile is None:
            raise ValidationError({"customer": "Customer profile required."})
        serializer.save(customer=profile)


@extend_schema_view(
    list=extend_schema(summary="List news articles", tags=["News"]),
    retrieve=extend_schema(summary="Retrieve news article", tags=["News"]),
    create=extend_schema(summary="Create news article", tags=["News"]),
    update=extend_schema(summary="Update news article", tags=["News"]),
    partial_update=extend_schema(summary="Partially update news article", tags=["News"]),
    destroy=extend_schema(summary="Delete news article", tags=["News"]),
)
class NewsArticleViewSet(viewsets.ModelViewSet):
    queryset = NewsArticle.objects.filter(is_deleted=False)
    serializer_class = NewsArticleSerializer
    permission_classes = [NewsPromoEditorOrReadOnly]
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NewsArticleAPIFilter
    search_fields = ("title", "slug", "body")
    ordering_fields = ("title", "slug", "published_at", "is_published", "created_at")
    ordering = ("-published_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "news"

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if not u.is_authenticated or not (u.is_staff or u.is_superuser):
            qs = qs.filter(is_published=True)
        return qs


@extend_schema_view(
    list=extend_schema(summary="List promo codes", tags=["Promo codes"]),
    retrieve=extend_schema(summary="Retrieve promo code", tags=["Promo codes"]),
    create=extend_schema(summary="Create promo code", tags=["Promo codes"]),
    update=extend_schema(summary="Update promo code", tags=["Promo codes"]),
    partial_update=extend_schema(summary="Partially update promo code", tags=["Promo codes"]),
    destroy=extend_schema(summary="Delete promo code", tags=["Promo codes"]),
)
class PromoCodeViewSet(viewsets.ModelViewSet):
    queryset = PromoCode.objects.filter(is_deleted=False).prefetch_related("customers")
    serializer_class = PromoCodeSerializer
    permission_classes = [NewsPromoEditorOrReadOnly]
    pagination_class = ZoomShopPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PromoCodeAPIFilter
    search_fields = ("code",)
    ordering_fields = ("code", "discount_percent", "valid_from", "valid_until", "created_at")
    ordering = ("-created_at",)
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "promocodes"

    def get_queryset(self):
        qs = super().get_queryset()
        u = self.request.user
        if not u.is_authenticated or not (u.is_staff or u.is_superuser):
            qs = qs.filter(is_active=True)
        return qs
