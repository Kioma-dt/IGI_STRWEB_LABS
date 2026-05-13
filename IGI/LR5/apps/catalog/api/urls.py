from __future__ import annotations

from django.urls import path

from apps.catalog.api.views import ProductListView, ProductManageView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="catalog-product-list"),
    path("products/manage/", ProductManageView.as_view(), name="catalog-product-manage"),
]
