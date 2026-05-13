from __future__ import annotations

from django.urls import path

from apps.orders.api.views import MyOrdersView, PlaceOrderView, SalesStatisticsView

urlpatterns = [
    path("mine/", MyOrdersView.as_view(), name="orders-mine"),
    path("place/", PlaceOrderView.as_view(), name="orders-place"),
    path("sales/stats/", SalesStatisticsView.as_view(), name="orders-sales-stats"),
]
