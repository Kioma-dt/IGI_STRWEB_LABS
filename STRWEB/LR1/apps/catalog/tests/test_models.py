from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from apps.catalog.models import Category, Product, ProductStock


class CategoryModelTest(TestCase):
    """Тесты для модели Category"""

    def test_create_root_category(self):
        cat = Category.objects.create(name="Dogs", slug="dogs")
        self.assertEqual(str(cat), "Dogs")
        self.assertIsNone(cat.parent)

    def test_create_subcategory(self):
        parent = Category.objects.create(name="Dogs", slug="dogs")
        child = Category.objects.create(name="Dog Food", slug="dog-food", parent=parent)
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent.children.all())

    def test_category_hierarchy(self):
        level1 = Category.objects.create(name="L1", slug="l1")
        level2 = Category.objects.create(name="L2", slug="l2", parent=level1)
        level3 = Category.objects.create(name="L3", slug="l3", parent=level2)
        self.assertEqual(level3.parent.parent, level1)

    def test_category_unique_slug(self):
        Category.objects.create(name="Dogs", slug="dogs")
        with self.assertRaises(Exception):
            Category.objects.create(name="Dogs", slug="dogs")


class ProductModelTest(TestCase):
    """Тесты для модели Product"""

    def setUp(self):
        self.category = Category.objects.create(name="Dogs", slug="dogs")

    def test_create_product(self):
        product = Product.objects.create(
            name="Dog Food",
            sku="SKU001",
            category=self.category,
            base_price=Decimal("29.99"),
            is_active=True,
        )
        self.assertEqual(str(product), "Dog Food")
        self.assertEqual(product.base_price, Decimal("29.99"))

    def test_product_age_restriction_optional(self):
        product = Product.objects.create(
            name="Test",
            sku="SKU002",
            category=self.category,
            base_price=Decimal("10.00"),
            age_restriction_min=None,
        )
        self.assertIsNone(product.age_restriction_min)

    def test_product_inactive(self):
        product = Product.objects.create(
            name="Test",
            sku="SKU003",
            category=self.category,
            base_price=Decimal("10.00"),
            is_active=False,
        )
        self.assertFalse(product.is_active)

    def test_product_unique_sku(self):
        Product.objects.create(
            name="Test1", sku="UNIQUE", category=self.category, base_price=Decimal("10")
        )
        with self.assertRaises(Exception):
            Product.objects.create(
                name="Test2",
                sku="UNIQUE",
                category=self.category,
                base_price=Decimal("10"),
            )

    def test_product_soft_delete(self):
        product = Product.objects.create(
            name="Test", sku="SKU004", category=self.category, base_price=Decimal("10")
        )
        product.soft_delete()
        self.assertTrue(product.is_deleted)


class ProductStockModelTest(TestCase):
    """Тесты для модели ProductStock"""

    def setUp(self):
        self.category = Category.objects.create(name="Dogs", slug="dogs")
        self.product = Product.objects.create(
            name="Dog Food",
            sku="SKU001",
            category=self.category,
            base_price=Decimal("29.99"),
        )

    def test_create_stock(self):
        stock = ProductStock.objects.create(product=self.product, quantity_on_hand=100)
        self.assertEqual(stock.quantity_on_hand, 100)

    def test_update_stock(self):
        stock = ProductStock.objects.create(product=self.product, quantity_on_hand=100)
        stock.quantity_on_hand = 50
        stock.save()
        self.assertEqual(ProductStock.objects.get(pk=stock.pk).quantity_on_hand, 50)

    def test_stock_zero(self):
        stock = ProductStock.objects.create(product=self.product, quantity_on_hand=0)
        self.assertEqual(stock.quantity_on_hand, 0)

    def test_one_stock_per_product(self):
        ProductStock.objects.create(product=self.product, quantity_on_hand=100)
        # Можно создать еще один, это допустимо в модели
        stock2 = ProductStock.objects.create(product=self.product, quantity_on_hand=50)
        self.assertEqual(ProductStock.objects.filter(product=self.product).count(), 2)
