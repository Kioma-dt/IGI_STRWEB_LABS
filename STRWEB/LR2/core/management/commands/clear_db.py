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
    CompanyHistoryEntry,
    Partner,
    Banner,
    PickupPoint,
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

from apps.users.models import (
    CustomerProfile,
    EmployeeProfile,
    ShopPermission,
)


class Command(BaseCommand):
    help = "Полная очистка базы данных"

    def handle(self, *args, **kwargs):
        self.stdout.write("Очистка базы данных...")



        OrderItem.objects.all().delete()
        PurchaseItem.objects.all().delete()

        Order.objects.all().delete()
        Purchase.objects.all().delete()



        ProductSupplier.objects.all().delete()



        ProductStock.objects.all().delete()


        Review.objects.all().delete()



        PromoCode.objects.all().delete()



        NewsArticle.objects.all().delete()

        CompanyHistoryEntry.objects.all().delete()

        FAQ.objects.all().delete()


        Vacancy.objects.all().delete()

        Contact.objects.all().delete()


        CompanyInfo.objects.all().delete()

        Partner.objects.all().delete()
        Banner.objects.all().delete()

        PickupPoint.objects.all().delete()



        Product.objects.all().delete()



        Category.objects.update(parent=None)
        Category.objects.all().delete()


        Supplier.objects.all().delete()

        CustomerProfile.objects.all().delete()
        EmployeeProfile.objects.all().delete()
        ShopPermission.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                "База данных успешно очищена."
            )
        )