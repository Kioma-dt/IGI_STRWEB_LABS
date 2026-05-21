from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.common.models import CompanyInfo, Contact, FAQ, Vacancy


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "sort_order", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("question", "answer")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    ordering = ("sort_order", "question")

    fieldsets = (
        (_("Вопрос / ответ"), {"fields": ("question", "answer", "sort_order")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "published_at", "is_deleted")
    list_filter = ("is_active", "is_deleted", "published_at")
    search_fields = ("title", "description")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    date_hierarchy = "published_at"

    fieldsets = (
        (_("Вакансия"), {"fields": ("title", "description")}),
        (_("Публикация"), {"fields": ("is_active", "published_at")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )

    actions = ("activate_vacancies", "deactivate_vacancies")

    @admin.action(description=_("Активировать"))
    def activate_vacancies(
        self,
        request: HttpRequest,
        queryset: QuerySet[Vacancy],
    ) -> None:
        queryset.update(is_active=True)

    @admin.action(description=_("Деактивировать"))
    def deactivate_vacancies(
        self,
        request: HttpRequest,
        queryset: QuerySet[Vacancy],
    ) -> None:
        queryset.update(is_active=False)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("type", "value", "is_primary", "is_deleted")
    list_filter = ("type", "is_primary", "is_deleted")
    search_fields = ("value",)
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Контакт"), {"fields": ("type", "value", "is_primary", "photo")}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "support_email", "phone", "is_current", "is_deleted")
    list_filter = ("is_current", "is_deleted")
    search_fields = ("name", "legal_address", "support_email", "phone")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Компания"), {"fields": ("name", "legal_address", "about")}),
        (_("Контакты"), {"fields": ("support_email", "phone")}),
        (_("Текущая запись"), {"fields": ("is_current",)}),
        (
            _("Системное"),
            {"fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at")},
        ),
    )
