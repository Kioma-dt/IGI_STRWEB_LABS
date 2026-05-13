from __future__ import annotations

from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

from apps.users.api.views_auth import (
    CsrfCookieView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
    SessionLoginView,
    SessionLogoutView,
    ZoomShopTokenObtainPairView,
)

urlpatterns = [
    path("csrf/", CsrfCookieView.as_view(), name="auth-csrf-cookie"),
    path("session/login/", SessionLoginView.as_view(), name="auth-session-login"),
    path("jwt/create/", ZoomShopTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/logout/", TokenBlacklistView.as_view(), name="jwt-logout"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("password/reset/", PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
    path("session/logout/", SessionLogoutView.as_view(), name="auth-session-logout"),
]
