from __future__ import annotations

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.news.models import NewsArticle


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "published_at", "is_deleted")
    list_filter = ("is_published", "is_deleted", "published_at")
    search_fields = ("title", "slug", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("id", "created_at", "updated_at", "deleted_at")
    date_hierarchy = "published_at"

    fieldsets = (
        (_("Статья"), {"fields": ("title", "slug", "summary", "body", "image")}),
        (_("Публикация"), {"fields": ("is_published", "published_at")}),
        (
            _("Системное"),
            {
                "fields": ("id", "is_deleted", "deleted_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    actions = ("publish_articles", "unpublish_articles")

    @admin.action(description=_("Опубликовать"))
    def publish_articles(
        self,
        request: HttpRequest,
        queryset: QuerySet[NewsArticle],
    ) -> None:
        queryset.update(is_published=True)

    @admin.action(description=_("Снять с публикации"))
    def unpublish_articles(
        self,
        request: HttpRequest,
        queryset: QuerySet[NewsArticle],
    ) -> None:
        queryset.update(is_published=False)
