from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path("auth/", include("apps.users.api.auth_urls")),
    path("common/", include("apps.common.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("suppliers/", include("apps.suppliers.urls")),
    path("orders/", include("apps.orders.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("promotions/", include("apps.promotions.urls")),
    path("news/", include("apps.news.urls")),
]
