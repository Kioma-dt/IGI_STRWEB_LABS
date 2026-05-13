from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.suppliers.models import ProductSupplier, Supplier


class ProductSupplierInline(admin.TabularInline):
    model = ProductSupplier
    fk_name = "supplier"
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("name", "phone", "email", "address")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    inlines = (ProductSupplierInline,)
    ordering = ("name",)

    fieldsets = (
        (_("Контакты"), {"fields": ("name", "phone", "email", "address")}),
        (_("Статус"), {"fields": ("is_active",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("deactivate_suppliers", "activate_suppliers")

    @admin.action(description=_("Деактивировать"))
    def deactivate_suppliers(
        self,
        request: HttpRequest,
        queryset: QuerySet[Supplier],
    ) -> None:
        queryset.update(is_active=False)

    @admin.action(description=_("Активировать"))
    def activate_suppliers(
        self,
        request: HttpRequest,
        queryset: QuerySet[Supplier],
    ) -> None:
        queryset.update(is_active=True)


@admin.register(ProductSupplier)
class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ("product", "supplier", "last_purchase_price", "is_deleted")
    list_filter = ("supplier", "is_deleted")
    search_fields = (
        "product__name",
        "product__sku",
        "supplier__name",
    )
    autocomplete_fields = ("product", "supplier")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Связь"), {"fields": ("product", "supplier", "last_purchase_price")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )
