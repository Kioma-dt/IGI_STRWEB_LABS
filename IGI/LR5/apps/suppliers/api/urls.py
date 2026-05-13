from __future__ import annotations

from django.urls import path

from apps.suppliers.api.views import SupplierListView

urlpatterns = [
    path("", SupplierListView.as_view(), name="suppliers-list"),
]
