from __future__ import annotations

from django.urls import path

from apps.promotions.api.views import ActivePromotionsListView

urlpatterns = [
    path("active/", ActivePromotionsListView.as_view(), name="promotions-active"),
]
