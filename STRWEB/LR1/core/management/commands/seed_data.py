from decimal import Decimal
from datetime import timedelta
from pathlib import Path
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

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
    PickupPoint,
    Partner,
    Banner,
)

from apps.news.models import(
    NewsArticle
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

from apps.reviews.models import(
    Review
)

from apps.suppliers.models import (
    Supplier,
    ProductSupplier,
)

from apps.users.models import (
    CustomerProfile,
    EmployeeProfile,
)


class Command(BaseCommand):
    help = "Заполнение базы тестовыми данными"

    def load_image(self):
        """Загружает изображение из media/images.jpeg"""
        image_path = settings.BASE_DIR / "media" / "images.jpeg"
        if image_path.exists():
            with open(image_path, "rb") as f:
                return SimpleUploadedFile(
                    "images.jpeg",
                    f.read(),
                    content_type="image/jpeg",
                )
        return None

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание тестовых данных...")



        dogs = Category.objects.create(
            name="Собаки",
            slug="dogs",
            description="Товары для собак",
        )

        cats = Category.objects.create(
            name="Кошки",
            slug="cats",
            description="Товары для кошек",
        )

        birds = Category.objects.create(
            name="Птицы",
            slug="birds",
            description="Товары для птиц",
        )

        rodents = Category.objects.create(
            name="Грызуны",
            slug="rodents",
            description="Товары для грызунов",
        )

        dog_food = Category.objects.create(
            name="Корм для собак",
            slug="dog-food",
            parent=dogs,
        )

        dog_toys = Category.objects.create(
            name="Игрушки для собак",
            slug="dog-toys",
            parent=dogs,
        )

        cat_food = Category.objects.create(
            name="Корм для кошек",
            slug="cat-food",
            parent=cats,
        )

        cat_toys = Category.objects.create(
            name="Игрушки для кошек",
            slug="cat-toys",
            parent=cats,
        )

        bird_food = Category.objects.create(
            name="Корм для птиц",
            slug="bird-food",
            parent=birds,
        )

        rodent_food = Category.objects.create(
            name="Корм для грызунов",
            slug="rodent-food",
            parent=rodents,
        )


        products = [
            Product.objects.create(
                name="Сухой корм для щенков",
                sku="SKU-001",
                category=dog_food,
                base_price=Decimal("79.90"),
                is_active=True,
            ),

            Product.objects.create(
                name="Корм для взрослых собак",
                sku="SKU-002",
                category=dog_food,
                base_price=Decimal("99.90"),
                is_active=True,
            ),

            Product.objects.create(
                name="Резиновый мячик",
                sku="SKU-003",
                category=dog_toys,
                base_price=Decimal("15.50"),
                is_active=True,
            ),

            Product.objects.create(
                name="Игрушечная косточка",
                sku="SKU-004",
                category=dog_toys,
                base_price=Decimal("18.00"),
                is_active=True,
            ),

            Product.objects.create(
                name="Корм с лососем для кошек",
                sku="SKU-005",
                category=cat_food,
                base_price=Decimal("25.00"),
                is_active=True,
            ),

            Product.objects.create(
                name="Сухой корм для котят",
                sku="SKU-006",
                category=cat_food,
                base_price=Decimal("28.00"),
                is_active=True,
            ),

            Product.objects.create(
                name="Игрушечная мышка",
                sku="SKU-007",
                category=cat_toys,
                base_price=Decimal("7.50"),
                is_active=True,
            ),

            Product.objects.create(
                name="Когтеточка большая",
                sku="SKU-008",
                category=cat_toys,
                base_price=Decimal("65.00"),
                is_active=True,
            ),

            Product.objects.create(
                name="Корм для попугаев",
                sku="SKU-009",
                category=bird_food,
                base_price=Decimal("12.90"),
                is_active=True,
            ),

            Product.objects.create(
                name="Корм для хомяков",
                sku="SKU-010",
                category=rodent_food,
                base_price=Decimal("9.90"),
                is_active=True,
            ),
        ]

        quantities = [120, 85, 300, 150, 90, 110, 400, 40, 130, 160]

        for product, qty in zip(products, quantities):
            ProductStock.objects.create(
                product=product,
                quantity_on_hand=qty,
            )


        suppliers = [
            Supplier.objects.create(
                name="БелЗооПоставка",
                phone="+375 (29) 111-11-11",
                email="belzoo@example.com",
                address="Минск",
                is_active=True,
            ),

            Supplier.objects.create(
                name="ПитомецТрейд",
                phone="+375 (29) 222-22-22",
                email="pitomectrade@example.com",
                address="Гомель",
                is_active=True,
            ),

            Supplier.objects.create(
                name="ЗооМир",
                phone="+375 (29) 333-33-33",
                email="zoomir@example.com",
                address="Брест",
                is_active=True,
            ),

            Supplier.objects.create(
                name="Лапки и Хвосты",
                phone="+375 (29) 444-44-44",
                email="lapki@example.com",
                address="Витебск",
                is_active=True,
            ),

            Supplier.objects.create(
                name="КормПоставка",
                phone="+375 (29) 555-55-55",
                email="korm@example.com",
                address="Могилев",
                is_active=True,
            ),
        ]



        ProductSupplier.objects.create(
            product=products[0],
            supplier=suppliers[0],
            last_purchase_price=Decimal("60.00"),
        )

        ProductSupplier.objects.create(
            product=products[1],
            supplier=suppliers[1],
            last_purchase_price=Decimal("75.00"),
        )

        ProductSupplier.objects.create(
            product=products[2],
            supplier=suppliers[2],
            last_purchase_price=Decimal("8.00"),
        )

        ProductSupplier.objects.create(
            product=products[3],
            supplier=suppliers[0],
            last_purchase_price=Decimal("10.00"),
        )

        ProductSupplier.objects.create(
            product=products[4],
            supplier=suppliers[1],
            last_purchase_price=Decimal("16.00"),
        )

        ProductSupplier.objects.create(
            product=products[5],
            supplier=suppliers[2],
            last_purchase_price=Decimal("18.00"),
        )

        ProductSupplier.objects.create(
            product=products[6],
            supplier=suppliers[3],
            last_purchase_price=Decimal("3.50"),
        )

        ProductSupplier.objects.create(
            product=products[7],
            supplier=suppliers[4],
            last_purchase_price=Decimal("40.00"),
        )

        ProductSupplier.objects.create(
            product=products[8],
            supplier=suppliers[0],
            last_purchase_price=Decimal("7.00"),
        )

        ProductSupplier.objects.create(
            product=products[9],
            supplier=suppliers[4],
            last_purchase_price=Decimal("5.00"),
        )

        faq_data = [
            ("Как оформить заказ?", "Добавьте товары в корзину и оформите заказ."),
            ("Можно ли вернуть товар?", "Да, в течение 14 дней."),
            ("Есть ли доставка?", "Да, доставка работает по всей стране."),
            ("Как оплатить заказ?", "Оплата картой или наличными."),
            ("Есть ли самовывоз?", "Да, доступен самовывоз."),
            ("Можно ли отменить заказ?", "Да, до отправки."),
            ("Когда приходит заказ?", "Обычно 1-3 дня."),
            ("Есть ли скидки?", "Да, следите за акциями."),
            ("Как связаться с поддержкой?", "Через почту или телефон."),
            ("Есть ли товары 18+?", "Да, некоторые позиции имеют ограничения."),
        ]

        for i, (q, a) in enumerate(faq_data):
            FAQ.objects.create(
                question=q,
                answer=a,
                sort_order=i,
            )


        vacancy_titles = [
            "Продавец-консультант",
            "Кассир",
            "Менеджер склада",
            "Курьер",
            "Оператор поддержки",
            "Контент-менеджер",
            "Маркетолог",
            "Администратор магазина",
            "Грузчик",
            "Менеджер закупок",
        ]

        for title in vacancy_titles:
            Vacancy.objects.create(
                title=title,
                description=f"Описание вакансии: {title}",
                is_active=True,
                published_at=timezone.now(),
            )



        image = self.load_image()

        Contact.objects.create(
            type="phone",
            value="+375 (29) 777-77-77",
            is_primary=True,
            photo=image if image else None,
        )

        Contact.objects.create(
            type="email",
            value="support@zooshop.by",
            is_primary=True,
            photo=image if image else None,
        )

        Contact.objects.create(
            type="address",
            value="г. Минск, ул. Центральная 10",
            is_primary=True,
            photo=image if image else None,
        )

        Contact.objects.create(
            type="social",
            value="@zooshop",
            is_primary=False,
            photo=image if image else None,
        )

        Contact.objects.create(
            type=Contact.ContactType.EMPLOYEE,
            value="ivanov-manager",
            employee_name="Иван Иванов",
            job_description="Менеджер зала: консультации по кормам и аксессуарам.",
            phone_number="+375 (29) 111-11-11",
            email_address="ivanov@zooshop.by",
            is_primary=False,
            photo=image if image else None,
        )

        Contact.objects.create(
            type=Contact.ContactType.EMPLOYEE,
            value="petrova-support",
            employee_name="Анна Петрова",
            job_description="Оператор поддержки: ответы на вопросы клиентов.",
            phone_number="+375 (29) 222-22-22",
            email_address="petrova@zooshop.by",
            is_primary=False,
            photo=image if image else None,
        )

        Contact.objects.create(
            type=Contact.ContactType.EMPLOYEE,
            value="sidorov-warehouse",
            employee_name="Пётр Сидоров",
            job_description="Кладовщик: комплектация заказов и самовывоз.",
            phone_number="+375 (29) 333-33-33",
            email_address="sidorov@zooshop.by",
            is_primary=False,
            photo=image if image else None,
        )


        company = CompanyInfo.objects.create(
            name="ЗооМаркет",
            legal_address="г. Минск, ул. Ленина 15",
            about="Сеть магазинов товаров для животных.",
            support_email="support@zooshop.by",
            phone="+375 (29) 888-88-88",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            requisites=(
                "ООО «ЗооМаркет»\n"
                "УНП 123456789\n"
                "р/с BY00UNBS00000000000000000000 в ОАО «Банк»\n"
                "BIC UNBSBY2X"
            ),
            certificate_text=(
                "Сертификат соответствия на розничную торговлю зоотоварами. "
                "Выдан уполномоченным органом. Действует на территории РБ."
            ),
            is_current=True,
            logo=image if image else None,
        )

        CompanyHistoryEntry.objects.create(
            company=company,
            year=2018,
            description="Открытие первого магазина в Минске.",
        )
        CompanyHistoryEntry.objects.create(
            company=company,
            year=2020,
            description="Запуск интернет-витрины и доставки.",
        )
        CompanyHistoryEntry.objects.create(
            company=company,
            year=2023,
            description="Расширение ассортимента и сети пунктов выдачи.",
        )

        partners_data = [
            ("Royal Canin", "https://www.royalcanin.com/"),
            ("Hills", "https://www.hillspet.com/"),
            ("Purina", "https://www.purina.com/"),
        ]
        for i, (pname, purl) in enumerate(partners_data):
            Partner.objects.create(
                name=pname,
                url=purl,
                logo=image if image else None,
                is_active=True,
                sort_order=i,
            )

        for i, title in enumerate(
            ("Весенняя акция", "Новинки для кошек", "Скидки на корма")
        ):
            Banner.objects.create(
                title=title,
                image=image if image else None,
                link_url="/shop/catalog/",
                is_active=True,
                sort_order=i,
            )


        for i in range(1, 11):
            PickupPoint.objects.create(
                name=f"Пункт выдачи №{i}",
                address=f"г. Минск, ул. Тестовая {i}",
                phone=f"+375 (29) {100+i:03d}-{10+i:02d}-{20+i:02d}",
                working_hours="09:00 - 21:00",
                is_active=True,
            )


        for i in range(1, 11):
            NewsArticle.objects.create(
                title=f"Новость магазина №{i}",
                slug=f"news-{i}",
                summary=f"Кратко: важные обновления зоомагазина №{i}.",
                body=f"Содержимое новости №{i}. Полный текст статьи для демонстрации раздела новостей.",
                published_at=timezone.now(),
                is_published=True,
                image=image if image else None,
            )



        promo_codes = []

        for i in range(1, 11):
            promo = PromoCode.objects.create(
                code=f"PROMO{i}",
                discount_percent=Decimal(str(i + 5)),
                valid_from=timezone.now().date(),
                valid_until=timezone.now().date() + timedelta(days=365),
                max_uses=100,
                current_uses=0,
                is_active=True,
            )

            promo_codes.append(promo)

        # Архивные промокоды (истёкшие / неактивные)
        PromoCode.objects.create(
            code="OLD2020",
            discount_percent=Decimal("10.00"),
            valid_from=timezone.now().date() - timedelta(days=800),
            valid_until=timezone.now().date() - timedelta(days=400),
            max_uses=50,
            current_uses=50,
            is_active=False,
        )
        PromoCode.objects.create(
            code="EXPIRED",
            discount_percent=Decimal("15.00"),
            valid_from=timezone.now().date() - timedelta(days=90),
            valid_until=timezone.now().date() - timedelta(days=1),
            max_uses=100,
            current_uses=10,
            is_active=True,
        )


        customer = CustomerProfile.objects.filter(is_deleted=False).first()
        employee = EmployeeProfile.objects.filter(is_deleted=False).first()



        if customer and employee:
            statuses = [
                Order.Status.NEW,
                Order.Status.PAID,
                Order.Status.SHIPPED,
                Order.Status.COMPLETED,
                Order.Status.CANCELLED,
            ]

            orders = []

            for i in range(10):
                order = Order.objects.create(
                    customer=customer,
                    created_by=employee,
                    promo_code=promo_codes[i % len(promo_codes)],
                    status=statuses[i % len(statuses)],
                    total_amount=Decimal("0.00"),
                )

                orders.append(order)

            for i, order in enumerate(orders):
                product = products[i % len(products)]

                qty = i + 1
                total = product.base_price * qty

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=product.base_price,
                    line_total=total,
                )

                order.total_amount = total
                order.save()


        purchases = []

        if employee:
            for i in range(10):
                purchase = Purchase.objects.create(
                    supplier=suppliers[i % len(suppliers)],
                    created_by=employee,
                )

                purchases.append(purchase)

            for i, purchase in enumerate(purchases):
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=products[i % len(products)],
                    quantity=(i + 1) * 10,
                    purchase_price=Decimal("10.00") + i,
                )


        if customer:
            for i in range(10):
                Review.objects.create(
                    product=products[i % len(products)],
                    customer=customer,
                    rating=(i % 5) + 1,
                    title=f"Отзыв №{i + 1}",
                    body=f"Очень хороший товар №{i + 1}",
                    is_published=True,
                )

        self.stdout.write(
            self.style.SUCCESS("Тестовые данные успешно созданы")
        )