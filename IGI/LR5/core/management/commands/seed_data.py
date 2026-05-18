from django.core.management.base import BaseCommand
from decimal import Decimal

from apps.catalog.models import Category, Product, ProductStock
from apps.orders.models import Order, OrderItem, Purchase, PurchaseItem
from apps.promotions.models import PromoCode
from apps.reviews.models import Review
from apps.news.models import NewsArticle
from apps.suppliers.models import Supplier, ProductSupplier
from apps.users.models import CustomerProfile, EmployeeProfile


class Command(BaseCommand):
    help = "Заполнение базы тестовыми данными"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание тестовых данных...")

        dogs = Category.objects.create(name="Собаки", slug="dogs")
        cats = Category.objects.create(name="Кошки", slug="cats")

        dog_food = Category.objects.create(name="Корм собак", slug="dog-food", parent=dogs)
        dog_toys = Category.objects.create(name="Игрушки собак", slug="dog-toys", parent=dogs)
        cat_food = Category.objects.create(name="Корм кошек", slug="cat-food", parent=cats)
        cat_toys = Category.objects.create(name="Игрушки кошек", slug="cat-toys", parent=cats)

        products = [
            Product.objects.create(name="Royal Canin Mini", sku="P1", category=dog_food, base_price=Decimal("80.00"), is_active=True),
            Product.objects.create(name="Pedigree Puppy", sku="P2", category=dog_food, base_price=Decimal("50.00"), is_active=True),
            Product.objects.create(name="Dog Ball", sku="P3", category=dog_toys, base_price=Decimal("10.00"), is_active=True),
            Product.objects.create(name="Dog Bone Toy", sku="P4", category=dog_toys, base_price=Decimal("12.00"), is_active=True),
            Product.objects.create(name="Whiskas Tuna", sku="P5", category=cat_food, base_price=Decimal("15.00"), is_active=True),
            Product.objects.create(name="Cat Dry Food", sku="P6", category=cat_food, base_price=Decimal("18.00"), is_active=True),
            Product.objects.create(name="Cat Mouse Toy", sku="P7", category=cat_toys, base_price=Decimal("6.00"), is_active=True),
            Product.objects.create(name="Scratching Post", sku="P8", category=cat_toys, base_price=Decimal("25.00"), is_active=True),
            Product.objects.create(name="Premium Dog Food", sku="P9", category=dog_food, base_price=Decimal("95.00"), is_active=True),
            Product.objects.create(name="Cat Premium Food", sku="P10", category=cat_food, base_price=Decimal("22.00"), is_active=True),
        ]

        for p in products:
            ProductStock.objects.create(product=p, quantity_on_hand=500)

        s1 = Supplier.objects.create(name="ZooTrade", phone="111", email="a@a.com", address="Minsk", is_active=True)
        s2 = Supplier.objects.create(name="PetFood", phone="222", email="b@b.com", address="Gomel", is_active=True)
        s3 = Supplier.objects.create(name="AnimalWorld", phone="333", email="c@c.com", address="Brest", is_active=True)

        ProductSupplier.objects.create(product=products[0], supplier=s1, last_purchase_price=Decimal("60"))
        ProductSupplier.objects.create(product=products[1], supplier=s1, last_purchase_price=Decimal("40"))
        ProductSupplier.objects.create(product=products[2], supplier=s2, last_purchase_price=Decimal("7"))
        ProductSupplier.objects.create(product=products[3], supplier=s3, last_purchase_price=Decimal("8"))
        ProductSupplier.objects.create(product=products[4], supplier=s2, last_purchase_price=Decimal("10"))
        ProductSupplier.objects.create(product=products[5], supplier=s3, last_purchase_price=Decimal("12"))
        ProductSupplier.objects.create(product=products[6], supplier=s1, last_purchase_price=Decimal("4"))
        ProductSupplier.objects.create(product=products[7], supplier=s1, last_purchase_price=Decimal("18"))

        customer = CustomerProfile.objects.filter(is_deleted=False).first()
        employee = EmployeeProfile.objects.filter(is_deleted=False).first()

        PromoCode.objects.create(
            code="WELCOME",
            discount_percent=10,
            valid_from="2026-01-01",
            valid_until="2027-01-01",
            max_uses=100,
            current_uses=0,
            is_active=True,
        )

        order1 = Order.objects.create(customer=customer, created_by=employee, status=Order.Status.NEW, total_amount=Decimal("0"))
        order2 = Order.objects.create(customer=customer, created_by=employee, status=Order.Status.PAID, total_amount=Decimal("0"))
        order3 = Order.objects.create(customer=customer, created_by=employee, status=Order.Status.SHIPPED, total_amount=Decimal("0"))
        order4 = Order.objects.create(customer=customer, created_by=employee, status=Order.Status.NEW, total_amount=Decimal("0"))
        order5 = Order.objects.create(customer=customer, created_by=employee, status=Order.Status.CANCELLED, total_amount=Decimal("0"))

        OrderItem.objects.create(order=order1, product=products[0], quantity=2, unit_price=products[0].base_price, line_total=products[0].base_price * 2)
        OrderItem.objects.create(order=order1, product=products[1], quantity=1, unit_price=products[1].base_price, line_total=products[1].base_price)

        OrderItem.objects.create(order=order2, product=products[2], quantity=5, unit_price=products[2].base_price, line_total=products[2].base_price * 5)

        OrderItem.objects.create(order=order3, product=products[3], quantity=3, unit_price=products[3].base_price, line_total=products[3].base_price * 3)
        OrderItem.objects.create(order=order3, product=products[4], quantity=1, unit_price=products[4].base_price, line_total=products[4].base_price)

        OrderItem.objects.create(order=order4, product=products[5], quantity=4, unit_price=products[5].base_price, line_total=products[5].base_price * 4)

        OrderItem.objects.create(order=order5, product=products[6], quantity=10, unit_price=products[6].base_price, line_total=products[6].base_price * 10)

        purchase = Purchase.objects.create(supplier=s1, created_by=employee)

        PurchaseItem.objects.create(purchase=purchase, product=products[0], quantity=100, purchase_price=Decimal("60"))
        PurchaseItem.objects.create(purchase=purchase, product=products[1], quantity=200, purchase_price=Decimal("40"))

        NewsArticle.objects.create(title="New delivery", slug="new-delivery", body="...", is_published=True)

        if customer:
            Review.objects.create(product=products[0], customer=customer, rating=5, title="Good", body="Nice", is_published=True)

        self.stdout.write(self.style.SUCCESS("Готово"))