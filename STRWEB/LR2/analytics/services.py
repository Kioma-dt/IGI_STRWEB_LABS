from __future__ import annotations

import base64
from datetime import datetime, timedelta
from decimal import Decimal
from io import BytesIO
from statistics import mean, median

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from django.db.models import Count, F, Q, Sum, Avg

from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.suppliers.models import Supplier, ProductSupplier

matplotlib.use("Agg")
sns.set_style("whitegrid")


class AnalyticsService:
    """Сервис расчёта статистики и аналитики магазина."""

    @staticmethod
    def get_popular_products(limit: int = 10):
        """Топ популярных товаров по количеству продаж."""
        return (
            Product.objects.filter(is_deleted=False)
            .annotate(
                total_sold=Sum("order_items__quantity", filter=Q(order_items__order__is_deleted=False))
            )
            .order_by("-total_sold")
            .values("id", "name", "sku", "base_price", "total_sold")[:limit]
        )

    @staticmethod
    def get_profitable_products(limit: int = 10):
        """Товары с максимальной прибылью."""
        products = []
        for item in (
            OrderItem.objects.select_related("product")
            .filter(order__is_deleted=False)
            .values("product")
            .annotate(
                total_revenue=Sum(F("line_total")),
                qty_sold=Sum("quantity"),
            )
            .order_by("-total_revenue")[:limit]
        ):
            product_id = item["product"]
            product = Product.objects.get(id=product_id)
            # Примерная закупочная цена (берём первый поставщик или 50% от цены продажи)
            supplier_price = (
                ProductSupplier.objects.filter(product_id=product_id)
                .values_list("last_purchase_price", flat=True)
                .first()
            )
            unit_cost = supplier_price or (product.base_price * Decimal("0.5"))
            
            total_cost = unit_cost * item["qty_sold"]
            profit = (item["total_revenue"] or 0) - total_cost
            
            products.append({
                "product_id": product_id,
                "name": product.name,
                "sku": product.sku,
                "revenue": item["total_revenue"] or Decimal("0"),
                "cost": total_cost,
                "profit": profit,
                "qty_sold": item["qty_sold"],
            })
        return products

    @staticmethod
    def get_sales_statistics():
        """Общая статистика по продажам."""
        orders = Order.objects.filter(is_deleted=False)
        total_orders = orders.count()
        total_revenue = OrderItem.objects.filter(
            order__is_deleted=False
        ).aggregate(
            total=Sum("line_total")
        )["total"] or Decimal("0")

        total_orders = Order.objects.filter(is_deleted=False).count()

        avg_order = (total_revenue / total_orders) if total_orders else Decimal("0")

        order_totals = (
            OrderItem.objects
            .filter(order__is_deleted=False)
            .values("order_id")
            .annotate(total=Sum("line_total"))
            .values_list("total", flat=True)
        )

        median_order = median(order_totals) if order_totals else 0
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "avg_order": avg_order,
            "median_order": Decimal(str(median_order)),
            "total_items_sold": OrderItem.objects.filter(order__is_deleted=False).aggregate(Sum("quantity"))["quantity__sum"] or 0,
        }

    @staticmethod
    def get_top_suppliers(limit: int = 10):
        """Топ поставщиков по объёму поставок (через товары)."""
        return (
            Supplier.objects.filter(is_deleted=False)
            .annotate(
                product_count=Count("products"),
                total_supplied=Sum(
                    "products__order_items__quantity",
                    filter=Q(products__order_items__order__is_deleted=False)
                ),
            )
            .order_by("-total_supplied")
            .values("id", "name", "phone", "address", "product_count", "total_supplied")[:limit]
        )

    @staticmethod
    def get_category_analytics():
        """Аналитика по категориям."""
        return (
            Category.objects.filter(is_deleted=False)
            .annotate(
                product_count=Count("products", filter=Q(products__is_deleted=False)),
                items_sold=Sum(
                    "products__order_items__quantity",
                    filter=Q(products__order_items__order__is_deleted=False),
                ),
                revenue=Sum(
                    "products__order_items__line_total",
                    filter=Q(products__order_items__order__is_deleted=False),
                ),
            )
            .order_by("-revenue")
            .values("id", "name", "product_count", "items_sold", "revenue")
        )

    @staticmethod
    def generate_sales_by_month_chart():
        """График продаж по месяцам (последние 12 месяцев)."""
        now = datetime.now()
        months_back = 12
        
        sales_by_month = {}
        for i in range(months_back, 0, -1):
            date = now - timedelta(days=30*i)
            month_key = date.strftime("%Y-%m")
            sales_by_month[month_key] = Decimal("0")
        
        orders = Order.objects.filter(
            is_deleted=False,
            ordered_at__gte=now - timedelta(days=365),
        ).values("ordered_at", "total_amount")
        
        for order in orders:
            month_key = order["ordered_at"].strftime("%Y-%m")
            if month_key in sales_by_month:
                sales_by_month[month_key] += order["total_amount"]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        months = list(sales_by_month.keys())
        amounts = [float(v) for v in sales_by_month.values()]
        
        ax.plot(months, amounts, marker="o", linewidth=2, markersize=6, color="#2E86AB")
        ax.fill_between(range(len(months)), amounts, alpha=0.3, color="#2E86AB")
        ax.set_xlabel("Месяц", fontsize=12)
        ax.set_ylabel("Выручка (руб.)", fontsize=12)
        ax.set_title("Продажи по месяцам", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return AnalyticsService._fig_to_base64(fig)

    @staticmethod
    def generate_popular_products_chart(limit: int = 10):
        """Диаграмма популярных товаров."""
        products = list(AnalyticsService.get_popular_products(limit))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        names = [p["name"] for p in products]
        sold = [p["total_sold"] or 0 for p in products]
        
        bars = ax.barh(names, sold, color="#A23B72")
        ax.set_xlabel("Количество продаж", fontsize=12)
        ax.set_title(f"Топ {limit} популярных товаров", fontsize=14, fontweight="bold")
        
        for bar in bars:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2, 
                   f"{int(bar.get_width())}", ha="left", va="center", fontweight="bold")
        
        plt.tight_layout()
        return AnalyticsService._fig_to_base64(fig)

    @staticmethod
    def generate_category_pie_chart():
        categories = list(AnalyticsService.get_category_analytics())

        fig, ax = plt.subplots(figsize=(10, 8))

        if not categories:
            ax.text(0.5, 0.5, "Нет данных", ha="center", va="center")
            ax.axis("off")
            return AnalyticsService._fig_to_base64(fig)

        names = [c["name"] for c in categories]
        items = [c["items_sold"] or 0 for c in categories]

        if sum(items) == 0:
            ax.text(0.5, 0.5, "Нет продаж", ha="center", va="center")
            ax.axis("off")
            return AnalyticsService._fig_to_base64(fig)

        colors = plt.cm.Set3(range(len(categories)))

        ax.pie(
            items,
            labels=names,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90
        )

        ax.set_title("Распределение продаж по категориям")

        plt.tight_layout()
        return AnalyticsService._fig_to_base64(fig)
    @staticmethod
    def generate_revenue_by_category_chart():
        """Столбчатая диаграмма выручки по категориям."""
        categories = list(AnalyticsService.get_category_analytics())
        
        fig, ax = plt.subplots(figsize=(12, 6))
        names = [c["name"] for c in categories]
        revenue = [float(c["revenue"] or 0) for c in categories]
        
        bars = ax.bar(names, revenue, color="#F18F01")
        ax.set_ylabel("Выручка (руб.)", fontsize=12)
        ax.set_title("Выручка по категориям", fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f"{int(height):,}", ha="center", va="bottom", fontweight="bold")
        
        plt.tight_layout()
        return AnalyticsService._fig_to_base64(fig)

    @staticmethod
    def generate_suppliers_chart(limit: int = 10):
        """Диаграмма топ поставщиков."""
        suppliers = list(AnalyticsService.get_top_suppliers(limit))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        names = [s["name"] for s in suppliers]
        supplied = [s["total_supplied"] or 0 for s in suppliers]
        
        bars = ax.barh(names, supplied, color="#06A77D")
        ax.set_xlabel("Количество поставлено", fontsize=12)
        ax.set_title(f"Топ {limit} поставщиков", fontsize=14, fontweight="bold")
        
        for bar in bars:
            ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2.,
                   f"{int(bar.get_width())}", ha="left", va="center", fontweight="bold")
        
        plt.tight_layout()
        return AnalyticsService._fig_to_base64(fig)

    @staticmethod
    def _fig_to_base64(fig):
        """Преобразует matplotlib фигуру в base64 строку для вложения в HTML."""
        buffer = BytesIO()
        fig.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{image_base64}"

