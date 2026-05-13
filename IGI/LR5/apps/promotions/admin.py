from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.promotions.models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_percent",
        "valid_from",
        "valid_until",
        "is_active",
        "current_uses",
        "max_uses",
        "is_deleted",
    )
    list_filter = ("is_active", "is_deleted", "valid_from", "valid_until")
    search_fields = ("code",)
    autocomplete_fields = ("customers",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (
            _("Промокод"),
            {"fields": ("code", "discount_percent", "is_active")},
        ),
        (_("Период"), {"fields": ("valid_from", "valid_until")}),
        (_("Лимиты"), {"fields": ("max_uses", "current_uses")}),
        (_("Клиенты"), {"fields": ("customers",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("reset_uses", "activate_promos", "deactivate_promos")

    @admin.action(description=_("Сбросить счётчик использований"))
    def reset_uses(
        self,
        request: HttpRequest,
        queryset: QuerySet[PromoCode],
    ) -> None:
        queryset.update(current_uses=0)

    @admin.action(description=_("Активировать"))
    def activate_promos(
        self,
        request: HttpRequest,
        queryset: QuerySet[PromoCode],
    ) -> None:
        queryset.update(is_active=True)

    @admin.action(description=_("Деактивировать"))
    def deactivate_promos(
        self,
        request: HttpRequest,
        queryset: QuerySet[PromoCode],
    ) -> None:
        queryset.update(is_active=False)
