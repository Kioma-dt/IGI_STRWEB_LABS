from __future__ import annotations

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

from analytics.services import AnalyticsService


class AdminOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Только администраторы могут просматривать аналитику."""
    
    login_url = "/admin/login/"
    
    def test_func(self) -> bool:
        return bool(self.request.user.is_superuser or self.request.user.is_staff)


class AnalyticsDashboardView(AdminOnlyMixin, TemplateView):
    """Главная страница аналитики со всеми статистиками и графиками."""
    
    template_name = "analytics/dashboard.html"
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # Общая статистика
        ctx["sales_stats"] = AnalyticsService.get_sales_statistics()
        
        # Популярные товары
        ctx["popular_products"] = AnalyticsService.get_popular_products(10)
        
        # Товары с максимальной прибылью
        ctx["profitable_products"] = AnalyticsService.get_profitable_products(10)
        
        # Топ поставщиков
        ctx["top_suppliers"] = AnalyticsService.get_top_suppliers(10)
        
        # Аналитика по категориям
        ctx["category_analytics"] = AnalyticsService.get_category_analytics()
        
        # Графики (base64 encoded images)
        ctx["sales_chart"] = AnalyticsService.generate_sales_by_month_chart()
        ctx["popular_chart"] = AnalyticsService.generate_popular_products_chart()
        ctx["category_pie_chart"] = AnalyticsService.generate_category_pie_chart()
        ctx["revenue_category_chart"] = AnalyticsService.generate_revenue_by_category_chart()
        ctx["suppliers_chart"] = AnalyticsService.generate_suppliers_chart()
        
        return ctx

