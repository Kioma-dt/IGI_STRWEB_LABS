from __future__ import annotations

from django.contrib import admin
from django.contrib.admin.exceptions import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.users.models import CustomerProfile, EmployeeProfile, ShopPermission

User = get_user_model()


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    extra = 0
    max_num = 1
    can_delete = True
    show_change_link = True
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")


class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    extra = 0
    max_num = 1
    can_delete = True
    show_change_link = True
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")


try:
    admin.site.unregister(User)
except NotRegistered:
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = (CustomerProfileInline, EmployeeProfileInline)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")

    fieldsets = DjangoUserAdmin.fieldsets
    add_fieldsets = DjangoUserAdmin.add_fieldsets


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "phone", "is_vip", "is_deleted")
    list_filter = ("is_vip", "is_deleted")
    search_fields = ("full_name", "phone", "user__username", "user__email")
    autocomplete_fields = ("user",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("full_name",)

    fieldsets = (
        (_("Профиль"), {"fields": ("user", "full_name", "birth_date", "phone", "is_vip")}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("toggle_vip",)

    @admin.action(description=_("Переключить VIP"))
    def toggle_vip(
        self,
        request: HttpRequest,
        queryset: QuerySet[CustomerProfile],
    ) -> None:
        for obj in queryset:
            obj.is_vip = not obj.is_vip
            obj.save(update_fields=["is_vip"])


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "user", "phone", "is_active", "is_deleted")
    list_filter = ("is_active", "is_deleted", "position")
    search_fields = ("full_name", "position", "phone", "user__username", "user__email")
    autocomplete_fields = ("user",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("full_name",)

    fieldsets = (
        (_("Сотрудник"), {"fields": ("user", "full_name", "position", "phone", "is_active")}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ShopPermission)
class ShopPermissionAdmin(admin.ModelAdmin):
    """
    Якорь для кастомных permissions (users.place_order и т.д.).
    Добавление строк не требуется — права задаются кодом модели.
    """

    list_display = ("__str__", "id")

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(
        self,
        request: HttpRequest,
        obj: ShopPermission | None = None,
    ) -> bool:
        return False

    def has_change_permission(
        self,
        request: HttpRequest,
        obj: ShopPermission | None = None,
    ) -> bool:
        return False
