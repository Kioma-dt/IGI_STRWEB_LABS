from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.orders.models import Order, OrderItem, Purchase, PurchaseItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at", "updated_at")


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0
    autocomplete_fields = ("product",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "status",
        "customer",
        "total_amount",
        "ordered_at",
        "is_deleted",
    )
    list_filter = ("status", "is_deleted", "ordered_at", "promo_code")
    search_fields = ("reference_number", "customer__full_name", "customer__phone")
    autocomplete_fields = ("customer", "created_by", "promo_code")
    readonly_fields = (
        "id",
        "reference_number",
        "ordered_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (OrderItemInline,)
    date_hierarchy = "ordered_at"
    ordering = ("-ordered_at",)

    fieldsets = (
        (
            _("Заказ"),
            {
                "fields": (
                    "reference_number",
                    "status",
                    "total_amount",
                    "ordered_at",
                )
            },
        ),
        (_("Участники"), {"fields": ("customer", "created_by", "promo_code")}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("mark_shipped", "mark_cancelled", "mark_completed")

    @admin.action(description=_("Статус: отгружен"))
    def mark_shipped(
        self,
        request: HttpRequest,
        queryset: QuerySet[Order],
    ) -> None:
        queryset.update(status=Order.Status.SHIPPED)

    @admin.action(description=_("Статус: отменён"))
    def mark_cancelled(
        self,
        request: HttpRequest,
        queryset: QuerySet[Order],
    ) -> None:
        queryset.update(status=Order.Status.CANCELLED)

    @admin.action(description=_("Статус: завершён"))
    def mark_completed(
        self,
        request: HttpRequest,
        queryset: QuerySet[Order],
    ) -> None:
        queryset.update(status=Order.Status.COMPLETED)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price", "line_total", "is_deleted")
    list_filter = ("is_deleted", "order__status")
    search_fields = ("order__reference_number", "product__name", "product__sku")
    autocomplete_fields = ("order", "product")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Позиция"), {"fields": ("order", "product", "quantity", "unit_price", "line_total")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "supplier",
        "ordered_at",
        "delivered_at",
        "created_by",
        "is_deleted",
    )
    list_filter = ("supplier", "is_deleted", "ordered_at")
    search_fields = ("reference_number", "supplier__name")
    autocomplete_fields = ("supplier", "created_by")
    readonly_fields = (
        "id",
        "reference_number",
        "ordered_at",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (PurchaseItemInline,)
    date_hierarchy = "ordered_at"
    ordering = ("-ordered_at",)

    fieldsets = (
        (
            _("Закупка"),
            {"fields": ("reference_number", "supplier", "ordered_at", "delivered_at")},
        ),
        (_("Сотрудник"), {"fields": ("created_by",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("mark_delivered_now",)

    @admin.action(description=_("Отметить доставленным (сейчас)"))
    def mark_delivered_now(
        self,
        request: HttpRequest,
        queryset: QuerySet[Purchase],
    ) -> None:
        queryset.update(delivered_at=timezone.now())


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("purchase", "product", "quantity", "purchase_price", "is_deleted")
    list_filter = ("is_deleted", "purchase__supplier")
    search_fields = ("purchase__reference_number", "product__sku", "product__name")
    autocomplete_fields = ("purchase", "product")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Строка"), {"fields": ("purchase", "product", "quantity", "purchase_price")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )
