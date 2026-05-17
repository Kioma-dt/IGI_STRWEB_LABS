from __future__ import annotations

from django.urls import path

from presentation.web import staff_views as views

app_name = "web_shop"

urlpatterns = [
    # path("", views.StaffPortalHomeView.as_view(), name="home"),
    # path("products/", views.ProductListView.as_view(), name="product-list"),
    # path("products/add/", views.ProductCreateView.as_view(), name="product-create"),
    # path("products/<uuid:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    # path(
    #     "products/<uuid:pk>/edit/",
    #     views.ProductUpdateView.as_view(),
    #     name="product-update",
    # ),
    # path(
    #     "products/<uuid:pk>/delete/",
    #     views.ProductDeleteView.as_view(),
    #     name="product-delete",
    # ),
    # path("suppliers/", views.SupplierListView.as_view(), name="supplier-list"),
    # path("suppliers/add/", views.SupplierCreateView.as_view(), name="supplier-create"),
    # path(
    #     "suppliers/<uuid:pk>/",
    #     views.SupplierDetailView.as_view(),
    #     name="supplier-detail",
    # ),
    # path(
    #     "suppliers/<uuid:pk>/edit/",
    #     views.SupplierUpdateView.as_view(),
    #     name="supplier-update",
    # ),
    # path(
    #     "suppliers/<uuid:pk>/delete/",
    #     views.SupplierDeleteView.as_view(),
    #     name="supplier-delete",
    # ),
    # path("orders/", views.OrderListView.as_view(), name="order-list"),
    # path("orders/add/", views.OrderCreateView.as_view(), name="order-create"),
    # path("orders/<uuid:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    # path(
    #     "orders/<uuid:pk>/edit/",
    #     views.OrderUpdateView.as_view(),
    #     name="order-update",
    # ),
    # path(
    #     "orders/<uuid:pk>/delete/",
    #     views.OrderDeleteView.as_view(),
    #     name="order-delete",
    # )
]
