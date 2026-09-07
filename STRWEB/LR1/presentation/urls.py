from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("", include("presentation.views.store.store_urls")),
    # path("admin/", include("presentation.web.admin_urls")),
]
