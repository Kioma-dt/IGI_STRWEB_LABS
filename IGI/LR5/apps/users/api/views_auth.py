from __future__ import annotations

import logging

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.serializers_auth import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    SessionLoginSerializer,
    ZoomShopTokenObtainPairSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class ZoomShopTokenObtainPairView(TokenObtainPairView):
    serializer_class = ZoomShopTokenObtainPairSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfCookieView(APIView):
    """Sets the CSRF cookie for browser clients (pair with session login POST)."""

    permission_classes = [AllowAny]
    authentication_classes: list[type] = []

    def get(self, request, *args, **kwargs) -> Response:
        return Response({"detail": "CSRF cookie set."})


class SessionLoginView(APIView):
    """Session-based login (Django session + CSRF middleware)."""

    permission_classes = [AllowAny]
    authentication_classes: list[type] = []

    def post(self, request, *args, **kwargs) -> Response:
        serializer = SessionLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        password = serializer.validated_data["password"]
        user = authenticate(request, username=email, password=password)
        if user is None or not user.is_active:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        return Response({"detail": "Logged in.", "user_id": user.id})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        return Response(
            {"id": user.id, "email": user.email},
            status=status.HTTP_201_CREATED,
        )


class PasswordResetRequestView(APIView):
    """Request a password reset token (email delivery depends on EMAIL_BACKEND)."""

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"].strip().lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user is not None:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            logger.info(
                "Password reset token issued user_id=%s uidb64=%s token=%s",
                user.pk,
                uid,
                token,
            )
        return Response(
            {"detail": "If the account exists, reset instructions have been processed."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]
        try:
            pk = int(urlsafe_base64_decode(uid).decode())
        except (ValueError, UnicodeDecodeError, TypeError):
            return Response({"detail": "Invalid uid."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(pk=pk, is_active=True).first()
        if user is None or not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(new_password)
        user.save(update_fields=["password"])
        logger.info("Password reset completed for user_id=%s", user.pk)
        return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)


class SessionLogoutView(APIView):
    """Clears Django session (browser clients using SessionAuthentication)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        request.session.flush()
        return Response(status=status.HTTP_204_NO_CONTENT)
