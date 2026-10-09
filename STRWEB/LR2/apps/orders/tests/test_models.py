from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from apps.orders.models import Order, OrderItem
from apps.catalog.models import Category, Product
from apps.users.models import CustomerProfile, EmployeeProfile
from django.contrib.auth.models import User


class OrderModelTest(TestCase):
    """Тесты для модели Order"""

    def setUp(self):
        self.customer_user = User.objects.create_user("customer", "c@test.com", "pass")
        self.employee_user = User.objects.create_user("employee", "e@test.com", "pass")
        self.customer = CustomerProfile.objects.create(user=self.customer_user)
        self.employee = EmployeeProfile.objects.create(user=self.employee_user)

    def test_create_order(self):
        order = Order.objects.create(
            customer=self.customer,
            created_by=self.employee,
            status=Order.Status.NEW,
            total_amount=Decimal("100.00"),
        )
        self.assertEqual(order.status, Order.Status.NEW)
        self.assertEqual(order.customer, self.customer)

    def test_order_status_choices(self):
        statuses = [
            Order.Status.NEW,
            Order.Status.PAID,
            Order.Status.SHIPPED,
            Order.Status.COMPLETED,
            Order.Status.CANCELLED,
        ]
        for status in statuses:
            order = Order.objects.create(
                customer=self.customer,
                created_by=self.employee,
                status=status,
                total_amount=Decimal("50.00"),
            )
            self.assertEqual(order.status, status)

    def test_order_total_amount(self):
        order = Order.objects.create(
            customer=self.customer,
            created_by=self.employee,
            total_amount=Decimal("99.99"),
        )
        self.assertEqual(order.total_amount, Decimal("99.99"))

    def test_order_with_promo_code(self):
        order = Order.objects.create(
            customer=self.customer,
            created_by=self.employee,
            promo_code_text="PROMO10",
            total_amount=Decimal("50.00"),
        )
        self.assertEqual(order.promo_code_text, "PROMO10")

    def test_order_soft_delete(self):
        order = Order.objects.create(
            customer=self.customer,
            created_by=self.employee,
            total_amount=Decimal("50.00"),
        )
        order.soft_delete()
        self.assertTrue(order.is_deleted)


class OrderItemModelTest(TestCase):
    """Тесты для модели OrderItem"""

    def setUp(self):
        self.customer_user = User.objects.create_user("customer", "c@test.com", "pass")
        self.employee_user = User.objects.create_user("employee", "e@test.com", "pass")
        self.customer = CustomerProfile.objects.create(user=self.customer_user)
        self.employee = EmployeeProfile.objects.create(user=self.employee_user)

        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Test Product", sku="TEST1", category=category, base_price=Decimal("50")
        )

        self.order = Order.objects.create(
            customer=self.customer,
            created_by=self.employee,
            total_amount=Decimal("100.00"),
        )

    def test_create_order_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            unit_price=Decimal("50.00"),
            line_total=Decimal("100.00"),
        )
        self.assertEqual(item.quantity, 2)
        self.assertEqual(item.line_total, Decimal("100.00"))

    def test_order_item_quantity_positive(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("25.00"),
        )
        self.assertGreater(item.quantity, 0)

    def test_multiple_items_in_order(self):
        category = Category.objects.create(name="Test2", slug="test2")
        product2 = Product.objects.create(
            name="Product2", sku="TEST2", category=category, base_price=Decimal("75")
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            unit_price=Decimal("50.00"),
        )
        OrderItem.objects.create(
            order=self.order,
            product=product2,
            quantity=1,
            unit_price=Decimal("75.00"),
        )

        self.assertEqual(self.order.items.count(), 2)
