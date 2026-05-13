from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse

from apps.users.constants import GROUP_ADMIN, GROUP_CUSTOMER, GROUP_EMPLOYEE

ViewFunc = TypeVar("ViewFunc", bound=Callable[..., HttpResponse])


def _in_group(user: Any, group_name: str) -> bool:
    return (
        user.is_authenticated
        and user.groups.filter(name=group_name).exists()
    )


def customer_required(
    view_func: ViewFunc,
    redirect_field_name: str = REDIRECT_FIELD_NAME,
    login_url: str | None = None,
) -> ViewFunc:
    """Django view decorator: authenticated user must be in `customer` group."""

    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                login_url or "/admin/login/",
                redirect_field_name,
            )
        if not _in_group(request.user, GROUP_CUSTOMER) and not request.user.is_superuser:
            raise PermissionDenied("Customer role required.")
        return view_func(request, *args, **kwargs)

    return _wrapped  # type: ignore[return-value]


def employee_required(
    view_func: ViewFunc,
    redirect_field_name: str = REDIRECT_FIELD_NAME,
    login_url: str | None = None,
) -> ViewFunc:
    """Django view decorator: staff, employee group, admin group, or superuser."""

    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                login_url or "/admin/login/",
                redirect_field_name,
            )
        u = request.user
        if u.is_superuser or u.is_staff:
            return view_func(request, *args, **kwargs)
        if _in_group(u, GROUP_EMPLOYEE) or _in_group(u, GROUP_ADMIN):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Employee role required.")

    return _wrapped  # type: ignore[return-value]


def admin_required(
    view_func: ViewFunc,
    redirect_field_name: str = REDIRECT_FIELD_NAME,
    login_url: str | None = None,
) -> ViewFunc:
    """Django view decorator: admin group or superuser."""

    @wraps(view_func)
    def _wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect_to_login(
                request.get_full_path(),
                login_url or "/admin/login/",
                redirect_field_name,
            )
        u = request.user
        if u.is_superuser or _in_group(u, GROUP_ADMIN):
            return view_func(request, *args, **kwargs)
        raise PermissionDenied("Admin role required.")

    return _wrapped  # type: ignore[return-value]


def login_and_customer_required(view_func: ViewFunc) -> ViewFunc:
    """Combines Django `login_required` with `customer_required`."""
    return login_required(customer_required(view_func))  # type: ignore[arg-type]
