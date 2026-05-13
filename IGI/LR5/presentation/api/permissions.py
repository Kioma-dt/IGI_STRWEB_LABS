from __future__ import annotations

from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


class IsStaffOrReadOnly(BasePermission):
    """Unsafe methods require an authenticated staff user."""

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        return bool(u and u.is_authenticated and u.is_staff)


class CatalogEditorOrReadOnly(BasePermission):
    """Public read; writes require manage_products, full_access, staff, or superuser."""

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser or u.is_staff:
            return True
        return u.has_perm("users.full_access") or u.has_perm("users.manage_products")


class NewsPromoEditorOrReadOnly(BasePermission):
    """Public read; writes require staff, superuser, or full_access."""

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if u.is_superuser or u.is_staff:
            return True
        return u.has_perm("users.full_access")
