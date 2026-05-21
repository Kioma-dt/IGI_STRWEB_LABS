from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
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

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание тестовых данных...")

        # =========================
        # Категории
        # =========================

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

        # =========================
        # Товары
        # =========================

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

        # =========================
        # Остатки
        # =========================

        quantities = [120, 85, 300, 150, 90, 110, 400, 40, 130, 160]

        for product, qty in zip(products, quantities):
            ProductStock.objects.create(
                product=product,
                quantity_on_hand=qty,
            )

        # =========================
        # Поставщики
        # =========================

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

        # =========================
        # ProductSupplier
        # =========================

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

        # =========================
        # FAQ
        # =========================

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

        # =========================
        # Вакансии
        # =========================

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

        # =========================
        # Контакты
        # =========================

        Contact.objects.create(
            type="phone",
            value="+375 (29) 777-77-77",
            is_primary=True,
        )

        Contact.objects.create(
            type="email",
            value="support@zooshop.by",
            is_primary=True,
        )

        Contact.objects.create(
            type="address",
            value="г. Минск, ул. Центральная 10",
            is_primary=True,
        )

        Contact.objects.create(
            type="social",
            value="@zooshop",
            is_primary=False,
        )

        # =========================
        # Информация о компании
        # =========================

        CompanyInfo.objects.create(
            name="ЗооМаркет",
            legal_address="г. Минск, ул. Ленина 15",
            about="Сеть магазинов товаров для животных.",
            support_email="support@zooshop.by",
            phone="+375 (29) 888-88-88",
            is_current=True,
        )

        # =========================
        # Пункты выдачи
        # =========================

        for i in range(1, 11):
            PickupPoint.objects.create(
                name=f"Пункт выдачи №{i}",
                address=f"г. Минск, ул. Тестовая {i}",
                phone=f"+375 (29) {100+i:03d}-{10+i:02d}-{20+i:02d}",
                working_hours="09:00 - 21:00",
                is_active=True,
            )

        # =========================
        # Новости
        # =========================

        for i in range(1, 11):
            NewsArticle.objects.create(
                title=f"Новость магазина №{i}",
                slug=f"news-{i}",
                body=f"Содержимое новости №{i}",
                published_at=timezone.now(),
                is_published=True,
            )

        # =========================
        # Промокоды
        # =========================

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

        # =========================
        # Пользователи
        # =========================

        customer = CustomerProfile.objects.filter(is_deleted=False).first()
        employee = EmployeeProfile.objects.filter(is_deleted=False).first()

        # =========================
        # Заказы
        # =========================

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

        # =========================
        # Закупки
        # =========================

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

        # =========================
        # Отзывы
        # =========================

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