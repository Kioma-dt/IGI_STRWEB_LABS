from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from presentation.api.viewsets import (
    CategoryViewSet,
    NewsArticleViewSet,
    OrderViewSet,
    ProductViewSet,
    PromoCodeViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("orders", OrderViewSet, basename="order")
router.register("reviews", ReviewViewSet, basename="review")
router.register("promocodes", PromoCodeViewSet, basename="promocode")
router.register("news", NewsArticleViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls)),
]
