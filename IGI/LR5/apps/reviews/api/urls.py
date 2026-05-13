from __future__ import annotations

from django.urls import path

from apps.reviews.api.views import ReviewCreateView

urlpatterns = [
    path("", ReviewCreateView.as_view(), name="reviews-create"),
]
