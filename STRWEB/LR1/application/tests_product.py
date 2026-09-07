from django.test import TestCase
from decimal import Decimal

from application.services.product_service import ProductService
from application.dto.product import RestockProductDTO, SetBasePriceDTO
from apps.catalog.models import Category, Product, ProductStock
from core.exceptions import BusinessValidationError, InsufficientStockError


class ProductServiceTest(TestCase):
    """Тесты для ProductService"""

    def setUp(self):
        self.service = ProductService()
        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Test Product", sku="SKU001", category=category, base_price=Decimal("50")
        )
        self.stock = ProductStock.objects.create(
            product=self.product, quantity_on_hand=100
        )

    def test_set_base_price(self):
        dto = SetBasePriceDTO(product_id=self.product.id, price=Decimal("75.50"))
        self.service.set_base_price(dto)
        updated = Product.objects.get(id=self.product.id)
        self.assertEqual(updated.base_price, Decimal("75.50"))

    def test_set_base_price_zero(self):
        dto = SetBasePriceDTO(product_id=self.product.id, price=Decimal("0"))
        self.service.set_base_price(dto)
        updated = Product.objects.get(id=self.product.id)
        self.assertEqual(updated.base_price, Decimal("0"))

    def test_restock_product(self):
        dto = RestockProductDTO(product_id=self.product.id, quantity=50)
        self.service.restock(dto)
        updated_stock = ProductStock.objects.get(product=self.product)
        self.assertEqual(updated_stock.quantity_on_hand, 150)

    def test_restock_to_zero(self):
        dto = RestockProductDTO(product_id=self.product.id, quantity=-100)
        self.service.restock(dto)
        updated_stock = ProductStock.objects.get(product=self.product)
        self.assertEqual(updated_stock.quantity_on_hand, 0)

    def test_check_stock_sufficient(self):
        result = self.service.check_stock(self.product.id, 50)
        self.assertTrue(result.has_sufficient_stock)
        self.assertEqual(result.available_quantity, 100)

    def test_check_stock_insufficient(self):
        result = self.service.check_stock(self.product.id, 150)
        self.assertFalse(result.has_sufficient_stock)

    def test_check_stock_zero_available(self):
        self.stock.quantity_on_hand = 0
        self.stock.save()
        result = self.service.check_stock(self.product.id, 1)
        self.assertFalse(result.has_sufficient_stock)
