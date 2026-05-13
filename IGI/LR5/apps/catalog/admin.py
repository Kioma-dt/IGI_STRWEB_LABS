from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.catalog.models import Category, Product, ProductStock
from apps.suppliers.models import ProductSupplier, Supplier


class SupplierListFilter(admin.SimpleListFilter):
    title = _("supplier")
    parameter_name = "supplier"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: admin.ModelAdmin,
    ) -> list[tuple[str, str]]:
        return [
            (str(pk), name)
            for pk, name in Supplier.objects.filter(is_deleted=False).values_list(
                "id",
                "name",
            )[:500]
        ]

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Product],
    ) -> QuerySet[Product]:
        if self.value():
            return queryset.filter(
                supplier_links__supplier_id=self.value(),
                supplier_links__is_deleted=False,
            ).distinct()
        return queryset


class ProductStockInline(admin.StackedInline):
    model = ProductStock
    extra = 0
    can_delete = False
    readonly_fields = ("created_at", "updated_at", "is_deleted", "deleted_at")


class ProductSupplierInline(admin.TabularInline):
    model = ProductSupplier
    fk_name = "product"
    extra = 0
    autocomplete_fields = ("supplier",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_deleted", "created_at")
    list_filter = ("is_deleted", "parent")
    search_fields = ("name", "slug", "description")
    autocomplete_fields = ("parent",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("name",)

    fieldsets = (
        (_("Основное"), {"fields": ("name", "slug", "parent")}),
        (_("Описание"), {"fields": ("description",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("mark_not_deleted", "soft_delete_selected")

    @admin.action(description=_("Восстановить (снять soft-delete)"))
    def mark_not_deleted(
        self,
        request: HttpRequest,
        queryset: QuerySet[Category],
    ) -> None:
        queryset.update(is_deleted=False, deleted_at=None)

    @admin.action(description=_("Пометить как удалённые (soft-delete)"))
    def soft_delete_selected(
        self,
        request: HttpRequest,
        queryset: QuerySet[Category],
    ) -> None:
        queryset.update(is_deleted=True, deleted_at=timezone.now())


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "image_thumb",
        "name",
        "sku",
        "category",
        "base_price",
        "is_active",
        "is_deleted",
    )
    list_filter = (
        "category",
        SupplierListFilter,
        "is_active",
        "age_restriction",
        "is_deleted",
    )
    search_fields = ("name", "sku", "description")
    autocomplete_fields = ("category",)
    readonly_fields = (
        "id",
        "image_thumb_large",
        "created_at",
        "updated_at",
        "deleted_at",
    )
    inlines = (ProductStockInline, ProductSupplierInline)
    ordering = ("name",)

    fieldsets = (
        (
            _("Товар"),
            {
                "fields": (
                    "name",
                    "sku",
                    "category",
                    "image",
                    "image_thumb_large",
                    "is_active",
                )
            },
        ),
        (
            _("Цена и ограничения"),
            {"fields": ("base_price", "age_restriction")},
        ),
        (_("Описание"), {"fields": ("description",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = (
        "make_active",
        "make_inactive",
        "soft_delete_products",
        "restore_products",
    )

    @admin.display(description=_("Фото"))
    def image_thumb(self, obj: Product) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" width="48" height="48" style="object-fit:contain;" alt="" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description=_("Предпросмотр"))
    def image_thumb_large(self, obj: Product) -> str:
        if obj.image:
            return format_html(
                '<img src="{}" width="200" style="max-height:200px;object-fit:contain;" alt="" />',
                obj.image.url,
            )
        return format_html("<span class='quiet'>{}</span>", _("Нет изображения"))

    @admin.action(description=_("Сделать активными"))
    def make_active(
        self,
        request: HttpRequest,
        queryset: QuerySet[Product],
    ) -> None:
        queryset.update(is_active=True)

    @admin.action(description=_("Сделать неактивными"))
    def make_inactive(
        self,
        request: HttpRequest,
        queryset: QuerySet[Product],
    ) -> None:
        queryset.update(is_active=False)

    @admin.action(description=_("Soft-delete выбранных"))
    def soft_delete_products(
        self,
        request: HttpRequest,
        queryset: QuerySet[Product],
    ) -> None:
        queryset.update(is_deleted=True, deleted_at=timezone.now())

    @admin.action(description=_("Восстановить выбранные"))
    def restore_products(
        self,
        request: HttpRequest,
        queryset: QuerySet[Product],
    ) -> None:
        queryset.update(is_deleted=False, deleted_at=None)


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity_on_hand", "is_deleted", "updated_at")
    list_filter = ("is_deleted",)
    search_fields = ("product__name", "product__sku")
    autocomplete_fields = ("product",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Склад"), {"fields": ("product", "quantity_on_hand")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )

    actions = ("zero_stock",)

    @admin.action(description=_("Обнулить остаток"))
    def zero_stock(
        self,
        request: HttpRequest,
        queryset: QuerySet[ProductStock],
    ) -> None:
        queryset.update(quantity_on_hand=0)
