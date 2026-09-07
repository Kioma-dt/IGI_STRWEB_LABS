from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/shop/', permanent=False)),
    path("admin/", include("presentation.views.admin.admin_urls")),
    path("shop/", include("presentation.views.store.store_urls")),
    path("analytics/", include("presentation.views.analytics.analytics_urls")),
]

# Подавать медиа файлы в development и контейнерах
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
