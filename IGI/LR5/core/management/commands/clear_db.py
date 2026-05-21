from django.core.management.base import BaseCommand

from apps.catalog.models import (
    Category,
    Product,
    ProductStock,
)

from apps.common.models import (
    FAQ,
    Vacancy,
    Contact,
    CompanyInfo,
    PickupPoint
)

from apps.suppliers.models import (
    Supplier,
    ProductSupplier,
)

from apps.orders.models import (
    Order,
    OrderItem,
    Purchase,
    PurchaseItem,
)

from apps.promotions.models import (
    PromoCode,
)

from apps.reviews.models import (
    Review,
)

from apps.news.models import (
    NewsArticle,
)


class Command(BaseCommand):
    help = "Полная очистка базы данных"

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка базы данных...")

        # =========================
        # Заказы и закупки
        # =========================

        OrderItem.objects.all().delete()
        PurchaseItem.objects.all().delete()

        Order.objects.all().delete()
        Purchase.objects.all().delete()

        # =========================
        # Связи поставщиков
        # =========================

        ProductSupplier.objects.all().delete()

        # =========================
        # Склады
        # =========================

        ProductStock.objects.all().delete()

        # =========================
        # Отзывы
        # =========================

        Review.objects.all().delete()

        # =========================
        # Промокоды
        # =========================

        PromoCode.objects.all().delete()

        # =========================
        # Новости
        # =========================

        NewsArticle.objects.all().delete()

        # =========================
        # FAQ
        # =========================

        FAQ.objects.all().delete()

        # =========================
        # Вакансии
        # =========================

        Vacancy.objects.all().delete()

        # =========================
        # Контакты
        # =========================

        Contact.objects.all().delete()

        # =========================
        # Информация о компании
        # =========================

        CompanyInfo.objects.all().delete()

        # =========================
        # Пункты выдачи
        # =========================

        PickupPoint.objects.all().delete()

        # =========================
        # Товары
        # =========================

        Product.objects.all().delete()

        # =========================
        # Категории
        # =========================

        Category.objects.update(parent=None)
        Category.objects.all().delete()

        # =========================
        # Поставщики
        # =========================

        Supplier.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "База данных успешно очищена."
            )
        )