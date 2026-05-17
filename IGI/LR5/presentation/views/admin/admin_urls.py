from __future__ import annotations

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from presentation.views.admin import admin_views as views

app_name = "admin_panel"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("admin_panel:product-list")),
        name="home",
    ),

    path("products/", views.AdminProductListView.as_view(), name="product-list"),
    path("products/add/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("products/<uuid:pk>/", views.AdminProductDetailView.as_view(), name="product-detail"),
    path("products/<uuid:pk>/edit/", views.AdminProductUpdateView.as_view(), name="product-update"),
    path("products/<uuid:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),

    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("categories/add/", views.CategoryCreateView.as_view(), name="category-create"),
    path(
        "categories/<uuid:pk>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/<uuid:pk>/edit/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "categories/<uuid:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),

    path("suppliers/", views.AdminSupplierListView.as_view(), name="supplier-list"),
    path("suppliers/add/", views.AdminSupplierCreateView.as_view(), name="supplier-create"),
    path("suppliers/<uuid:pk>/", views.AdminSupplierDetailView.as_view(), name="supplier-detail"),
    path("suppliers/<uuid:pk>/edit/", views.AdminSupplierUpdateView.as_view(), name="supplier-update"),
    path("suppliers/<uuid:pk>/delete/", views.AdminSupplierDeleteView.as_view(), name="supplier-delete"),


    path("sales/", views.AdminSalesListView.as_view(), name="sales-list"),
    path("sales/<uuid:pk>/", views.AdminSalesDetailView.as_view(), name="sales-detail"),

    path("reviews/", views.ReviewListView.as_view(), name="review-list"),
    path("reviews/add/", views.ReviewCreateView.as_view(), name="review-create"),
    path("reviews/<uuid:pk>/", views.ReviewDetailView.as_view(), name="review-detail"),
    path(
        "reviews/<uuid:pk>/edit/",
        views.ReviewUpdateView.as_view(),
        name="review-update",
    ),
    path(
        "reviews/<uuid:pk>/delete/",
        views.ReviewDeleteView.as_view(),
        name="review-delete",
    ),
    path("news/", views.NewsArticleListView.as_view(), name="news-list"),
    path("news/add/", views.NewsArticleCreateView.as_view(), name="news-create"),
    path(
        "news/<uuid:pk>/",
        views.NewsArticleDetailView.as_view(),
        name="news-detail",
    ),
    path(
        "news/<uuid:pk>/edit/",
        views.NewsArticleUpdateView.as_view(),
        name="news-update",
    ),
    path(
        "news/<uuid:pk>/delete/",
        views.NewsArticleDeleteView.as_view(),
        name="news-delete",
    ),
    path("promos/", views.PromoCodeListView.as_view(), name="promo-list"),
    path("promos/add/", views.PromoCodeCreateView.as_view(), name="promo-create"),
    path(
        "promos/<uuid:pk>/",
        views.PromoCodeDetailView.as_view(),
        name="promo-detail",
    ),
    path(
        "promos/<uuid:pk>/edit/",
        views.PromoCodeUpdateView.as_view(),
        name="promo-update",
    ),
    path(
        "promos/<uuid:pk>/delete/",
        views.PromoCodeDeleteView.as_view(),
        name="promo-delete",
    ),
]
