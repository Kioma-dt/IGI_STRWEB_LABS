from apps.catalog.models import Product, Category, ProductStock
from apps.suppliers.models import Supplier, ProductSupplier
from apps.orders.models import Order, OrderItem, Purchase, PurchaseItem
from apps.promotions.models import PromoCode
from apps.reviews.models import Review
from apps.news.models import NewsArticle

from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Полная очистка базы данных"

    def handle(self, *args, **kwargs):
        OrderItem.objects.all().delete()
        PurchaseItem.objects.all().delete()

        Order.objects.all().delete()
        Purchase.objects.all().delete()

        ProductSupplier.objects.all().delete()
        ProductStock.objects.all().delete()

        Review.objects.all().delete()
        NewsArticle.objects.all().delete()
        PromoCode.objects.all().delete()

        Product.objects.all().delete()

        Category.objects.update(parent=None)
        Category.objects.all().delete()

        Supplier.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS("База данных успешно очищена.")
        )