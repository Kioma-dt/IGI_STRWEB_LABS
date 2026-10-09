from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    label = "core"
    verbose_name = "Core (shared abstractions)"

    def ready(self) -> None:
        from django.contrib import admin

        from application.services.statistics_service import StatisticsService

        admin.site.site_header = "Зоомагазин — администрирование"
        admin.site.site_title = "ZoomShop Admin"
        admin.site.index_title = "Панель управления"
        admin.site.index_template = "admin/zooshop_index.html"

        _orig_index = admin.site.index

        def index_with_stats(request, extra_context=None):
            extra_context = extra_context or {}
            try:
                extra_context["shop_stats"] = (
                    StatisticsService().get_shop_statistics()
                )
            except Exception:
                extra_context["shop_stats"] = None
            return _orig_index(request, extra_context)

        admin.site.index = index_with_stats  # type: ignore[method-assign]
