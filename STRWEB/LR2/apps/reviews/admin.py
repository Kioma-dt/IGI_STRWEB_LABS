from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "customer", "rating", "title", "is_published", "is_deleted")
    list_filter = ("rating", "is_published", "is_deleted", "product__category")
    search_fields = ("title", "body", "product__name", "customer__full_name")
    autocomplete_fields = ("product", "customer")
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")

    fieldsets = (
        (_("Отзыв"), {"fields": ("product", "customer", "rating", "title", "body")}),
        (_("Модерация"), {"fields": ("is_published",)}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("publish_reviews", "unpublish_reviews")

    @admin.action(description=_("Опубликовать"))
    def publish_reviews(
        self,
        request: HttpRequest,
        queryset: QuerySet[Review],
    ) -> None:
        queryset.update(is_published=True)

    @admin.action(description=_("Снять с публикации"))
    def unpublish_reviews(
        self,
        request: HttpRequest,
        queryset: QuerySet[Review],
    ) -> None:
        queryset.update(is_published=False)
