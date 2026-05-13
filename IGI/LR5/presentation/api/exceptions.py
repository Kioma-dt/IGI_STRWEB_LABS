from __future__ import annotations

import logging
from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def zoomshop_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """
    Wraps DRF's default handler with a stable JSON envelope and sensible codes.

    Shape: ``{"detail": ..., "code": "...", "status": <http_status>}``
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        detail = response.data
        if isinstance(detail, dict) and len(detail) == 1 and "detail" in detail:
            detail = detail["detail"]
        code = getattr(exc, "default_code", "error")
        if isinstance(exc, APIException):
            code = getattr(exc, "default_code", code)
        response.data = {
            "detail": detail,
            "code": str(code),
            "status": response.status_code,
        }
        return response

    if isinstance(exc, Http404):
        return Response(
            {"detail": "Not found.", "code": "not_found", "status": status.HTTP_404_NOT_FOUND},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, DjangoPermissionDenied):
        return Response(
            {
                "detail": str(exc) or "Permission denied.",
                "code": "permission_denied",
                "status": status.HTTP_403_FORBIDDEN,
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    logger.exception("Unhandled API exception: %s", exc)
    return Response(
        {
            "detail": "Internal server error.",
            "code": "server_error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
