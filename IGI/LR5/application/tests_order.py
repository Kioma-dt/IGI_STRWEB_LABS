from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User

from application.services.order_service import OrderService
from application.dto.orders import OrderLineInputDTO, PlaceOrderDTO
from apps.catalog.models import Category, Product, ProductStock
from apps.suppliers.models import Supplier, ProductSupplier
from apps.users.models import CustomerProfile, EmployeeProfile
from apps.orders.models import Order
from core.exceptions import InsufficientStockError, BusinessValidationError


class OrderServiceTest(TestCase):
    """Тесты для OrderService"""

    def setUp(self):
        self.service = OrderService()

        # Setup customer and employee
        customer_user = User.objects.create_user("customer", "c@test.com", "pass")
        employee_user = User.objects.create_user("employee", "e@test.com", "pass")
        self.customer = CustomerProfile.objects.create(user=customer_user)
        self.employee = EmployeeProfile.objects.create(user=employee_user)

        # Setup product
        category = Category.objects.create(name="Dogs", slug="dogs")
        self.product = Product.objects.create(
            name="Dog Food", sku="SKU001", category=category, base_price=Decimal("50")
        )
        ProductStock.objects.create(product=self.product, quantity_on_hand=100)

        # Setup supplier
        self.supplier = Supplier.objects.create(
            name="Supplier", phone="+375291111111", email="s@test.com", address="Addr"
        )
        ProductSupplier.objects.create(
            product=self.product,
            supplier=self.supplier,
            last_purchase_price=Decimal("40"),
        )

    def test_place_order_single_item(self):
        lines = (
            OrderLineInputDTO(product_id=self.product.id, quantity=5),
        )
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=lines,
            promo_code=None,
            created_by_employee_id=self.employee.id,
        )

        result = self.service.place_order(dto)

        self.assertIsNotNone(result.reference_number)
        self.assertEqual(result.total, Decimal("250"))  # 5 * 50
        self.assertEqual(Order.objects.count(), 1)

    def test_place_order_multiple_items(self):
        category = Category.objects.create(name="Cats", slug="cats")
        product2 = Product.objects.create(
            name="Cat Food", sku="SKU002", category=category, base_price=Decimal("30")
        )
        ProductStock.objects.create(product=product2, quantity_on_hand=100)

        lines = (
            OrderLineInputDTO(product_id=self.product.id, quantity=2),
            OrderLineInputDTO(product_id=product2.id, quantity=3),
        )
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=lines,
            promo_code=None,
            created_by_employee_id=self.employee.id,
        )

        result = self.service.place_order(dto)
        self.assertEqual(result.total, Decimal("190"))  # (2*50) + (3*30)

    def test_place_order_insufficient_stock(self):
        lines = (
            OrderLineInputDTO(product_id=self.product.id, quantity=150),  # More than available
        )
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=lines,
            promo_code=None,
            created_by_employee_id=self.employee.id,
        )

        with self.assertRaises(InsufficientStockError):
            self.service.place_order(dto)


    def test_order_reduces_stock(self):
        initial_stock = ProductStock.objects.get(product=self.product).quantity_on_hand

        lines = (
            OrderLineInputDTO(product_id=self.product.id, quantity=10),
        )
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=lines,
            promo_code=None,
            created_by_employee_id=self.employee.id,
        )

        self.service.place_order(dto)
        updated_stock = ProductStock.objects.get(product=self.product).quantity_on_hand
        self.assertEqual(updated_stock, initial_stock - 10)
