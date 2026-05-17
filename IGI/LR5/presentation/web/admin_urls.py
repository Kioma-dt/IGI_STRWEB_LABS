from __future__ import annotations

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from presentation.web import admin_views as views

app_name = "admin_panel"

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url=reverse_lazy("admin_panel:product-list")),
        name="home",
    ),
    # Products
    path("products/", views.AdminProductListView.as_view(), name="product-list"),
    path("products/add/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("products/<uuid:pk>/", views.AdminProductDetailView.as_view(), name="product-detail"),
    path("products/<uuid:pk>/edit/", views.AdminProductUpdateView.as_view(), name="product-update"),
    path("products/<uuid:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),

    # Suppliers
    path("suppliers/", views.AdminSupplierListView.as_view(), name="supplier-list"),
    path("suppliers/add/", views.AdminSupplierCreateView.as_view(), name="supplier-create"),
    path("suppliers/<uuid:pk>/", views.AdminSupplierDetailView.as_view(), name="supplier-detail"),
    path("suppliers/<uuid:pk>/edit/", views.AdminSupplierUpdateView.as_view(), name="supplier-update"),
    path("suppliers/<uuid:pk>/delete/", views.AdminSupplierDeleteView.as_view(), name="supplier-delete"),

    # Sales (Orders)
    path("sales/", views.AdminSalesListView.as_view(), name="sales-list"),
    path("sales/<uuid:pk>/", views.AdminSalesDetailView.as_view(), name="sales-detail"),
]
