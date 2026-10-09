from __future__ import annotations

from django.urls import path

from presentation.views.analytics import analytic_views as views

app_name = "analytics"

urlpatterns = [
    path("", views.AnalyticsDashboardView.as_view(), name="dashboard"),
]

