from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

from apps.users.constants import GROUP_ADMIN, GROUP_CUSTOMER, GROUP_EMPLOYEE

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


def _user_groups(user: AbstractUser) -> set[str]:
    if not user.is_authenticated:
        return set()
    return set(user.groups.values_list("name", flat=True))


class IsSuperuser(BasePermission):
    """Django superuser (full admin panel + API bypass when combined)."""

    def has_permission(self, request, view) -> bool:
        u = request.user
        return bool(u and u.is_authenticated and u.is_superuser)


class IsAdminGroupOrSuperuser(BasePermission):
    """Admin group members or superuser."""

    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        return GROUP_ADMIN in _user_groups(u) or u.is_staff


class IsEmployeeRole(BasePermission):
    """Employee group, staff, admin group, or superuser."""

    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser or u.is_staff:
            return True
        groups = _user_groups(u)
        return GROUP_EMPLOYEE in groups or GROUP_ADMIN in groups


class IsCustomerRole(BasePermission):
    """Customer group (typical shopper)."""

    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        return GROUP_CUSTOMER in _user_groups(u)


def django_permission(perm: str) -> type[BasePermission]:
    """
    Factory: returns a DRF permission class that checks Django's auth.Permission.

    Example: ``permission_classes = [IsAuthenticated, django_permission("users.place_order")]``
    """

    perm_str = perm

    class _DjangoPermission(BasePermission):
        def has_permission(self, request, view) -> bool:
            u = request.user
            if not u or not u.is_authenticated:
                return False
            if u.is_superuser:
                return True
            if u.has_perm("users.full_access"):
                return True
            return u.has_perm(perm_str)

    _DjangoPermission.__name__ = f"DjangoPermission_{perm_str.replace('.', '_')}"
    return _DjangoPermission


    """Customer with Django permission to place orders."""

    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        if u.has_perm("users.full_access"):
            return True
        return u.has_perm("users.place_order")


class IsEmployeeWithSalesPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser or u.is_staff:
            return True
        if u.has_perm("users.full_access"):
            return True
        return u.has_perm("users.view_sales")
