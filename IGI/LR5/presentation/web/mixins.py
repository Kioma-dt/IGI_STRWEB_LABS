from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Back-office CRUD is limited to Django staff users."""

    login_url = "/admin/login/"

    def test_func(self) -> bool:
        u = self.request.user
        return bool(u.is_authenticated and u.is_staff)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Admin-only access: superuser or admin group member."""

    login_url = "/admin/login/"

    def test_func(self) -> bool:
        u = self.request.user
        if not u.is_authenticated:
            return False
        if u.is_superuser:
            return True
        # Check if user is in admin group
        return u.groups.filter(name="admin").exists()


class StaffFilterListContextMixin:
    """
    Adds querystring fragments for sort links while preserving django-filter params.
    Subclasses may define ``sort_links`` as tuple[tuple[str, str], ...] (ordering, label).
    """

    sort_links: tuple[tuple[str, str], ...] = ()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.request.GET.copy()
        p.pop("page", None)
        p.pop("ordering", None)
        ctx["non_order_query"] = p.urlencode()
        p2 = self.request.GET.copy()
        p2.pop("page", None)
        ctx["non_page_query"] = p2.urlencode()
        ctx["current_ordering"] = (self.request.GET.get("ordering") or "").strip()
        ctx["sort_links"] = getattr(self, "sort_links", ())
        return ctx
