from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("presentation.web.store_urls")),
    path("staff/", include("presentation.web.staff_urls")),
]
