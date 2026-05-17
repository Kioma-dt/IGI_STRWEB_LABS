from __future__ import annotations

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/shop/', permanent=False)),
    path("admin/", include("presentation.web.admin_urls")),
    path("shop/", include("presentation.web.urls")),
    path("analytics/", include("analytics.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
