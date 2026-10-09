from __future__ import annotations

from django.urls import re_path, reverse_lazy
from django.views.generic import RedirectView

from presentation.views.admin import admin_views as views

app_name = "admin_panel"

UUID = r"(?P<pk>[0-9a-fA-F-]{36})"


urlpatterns = [
    re_path(
        r"^$",
        RedirectView.as_view(url=reverse_lazy("admin_panel:product-list")),
        name="home",
    ),


    re_path(r"^products/$", views.AdminProductListView.as_view(), name="product-list"),
    re_path(r"^products/add/$", views.AdminProductCreateView.as_view(), name="product-create"),
    re_path(rf"^products/{UUID}/$", views.AdminProductDetailView.as_view(), name="product-detail"),
    re_path(rf"^products/{UUID}/edit/$", views.AdminProductUpdateView.as_view(), name="product-update"),
    re_path(rf"^products/{UUID}/delete/$", views.AdminProductDeleteView.as_view(), name="product-delete"),


    re_path(r"^categories/$", views.CategoryListView.as_view(), name="category-list"),
    re_path(r"^categories/add/$", views.CategoryCreateView.as_view(), name="category-create"),
    re_path(rf"^categories/{UUID}/$", views.CategoryDetailView.as_view(), name="category-detail"),
    re_path(rf"^categories/{UUID}/edit/$", views.CategoryUpdateView.as_view(), name="category-update"),
    re_path(rf"^categories/{UUID}/delete/$", views.CategoryDeleteView.as_view(), name="category-delete"),


    re_path(r"^suppliers/$", views.AdminSupplierListView.as_view(), name="supplier-list"),
    re_path(r"^suppliers/add/$", views.AdminSupplierCreateView.as_view(), name="supplier-create"),
    re_path(rf"^suppliers/{UUID}/$", views.AdminSupplierDetailView.as_view(), name="supplier-detail"),
    re_path(rf"^suppliers/{UUID}/edit/$", views.AdminSupplierUpdateView.as_view(), name="supplier-update"),
    re_path(rf"^suppliers/{UUID}/delete/$", views.AdminSupplierDeleteView.as_view(), name="supplier-delete"),


    re_path(r"^sales/$", views.AdminSalesListView.as_view(), name="sales-list"),
    re_path(rf"^sales/{UUID}/$", views.AdminSalesDetailView.as_view(), name="sales-detail"),

    re_path(r"^reviews/$", views.ReviewListView.as_view(), name="review-list"),
    re_path(r"^reviews/add/$", views.ReviewCreateView.as_view(), name="review-create"),
    re_path(rf"^reviews/{UUID}/$", views.ReviewDetailView.as_view(), name="review-detail"),
    re_path(rf"^reviews/{UUID}/edit/$", views.ReviewUpdateView.as_view(), name="review-update"),
    re_path(rf"^reviews/{UUID}/delete/$", views.ReviewDeleteView.as_view(), name="review-delete"),


    re_path(r"^news/$", views.NewsArticleListView.as_view(), name="news-list"),
    re_path(r"^news/add/$", views.NewsArticleCreateView.as_view(), name="news-create"),
    re_path(rf"^news/{UUID}/$", views.NewsArticleDetailView.as_view(), name="news-detail"),
    re_path(rf"^news/{UUID}/edit/$", views.NewsArticleUpdateView.as_view(), name="news-update"),
    re_path(rf"^news/{UUID}/delete/$", views.NewsArticleDeleteView.as_view(), name="news-delete"),


    re_path(r"^promos/$", views.PromoCodeListView.as_view(), name="promo-list"),
    re_path(r"^promos/add/$", views.PromoCodeCreateView.as_view(), name="promo-create"),
    re_path(rf"^promos/{UUID}/$", views.PromoCodeDetailView.as_view(), name="promo-detail"),
    re_path(rf"^promos/{UUID}/edit/$", views.PromoCodeUpdateView.as_view(), name="promo-update"),
    re_path(rf"^promos/{UUID}/delete/$", views.PromoCodeDeleteView.as_view(), name="promo-delete"),
]