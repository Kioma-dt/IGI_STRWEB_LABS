from django.test import TestCase
from decimal import Decimal

from apps.suppliers.models import Supplier, ProductSupplier
from apps.catalog.models import Category, Product


class SupplierModelTest(TestCase):
    """Тесты для модели Supplier"""

    def test_create_supplier(self):
        supplier = Supplier.objects.create(
            name="Test Supplier",
            phone="+375291111111",
            email="supplier@test.com",
            address="123 Main St",
            is_active=True,
        )
        self.assertEqual(str(supplier), "Test Supplier")
        self.assertTrue(supplier.is_active)

    def test_supplier_inactive(self):
        supplier = Supplier.objects.create(
            name="Inactive",
            phone="+375291111111",
            email="test@test.com",
            address="Addr",
            is_active=False,
        )
        self.assertFalse(supplier.is_active)

    def test_supplier_contact_info(self):
        supplier = Supplier.objects.create(
            name="Supplier",
            phone="+375291111111",
            email="s@test.com",
            address="123 Test Ave",
        )
        self.assertEqual(supplier.phone, "+375291111111")
        self.assertEqual(supplier.email, "s@test.com")
        self.assertEqual(supplier.address, "123 Test Ave")

    def test_supplier_soft_delete(self):
        supplier = Supplier.objects.create(
            name="Delete",
            phone="+375291111111",
            email="d@test.com",
            address="Addr",
        )
        supplier.soft_delete()
        self.assertTrue(supplier.is_deleted)


class ProductSupplierModelTest(TestCase):
    """Тесты для модели ProductSupplier"""

    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier", phone="+375291111111", email="s@test.com", address="Addr"
        )
        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Product", sku="SKU1", category=category, base_price=Decimal("100")
        )

    def test_create_product_supplier(self):
        ps = ProductSupplier.objects.create(
            product=self.product,
            supplier=self.supplier,
            last_purchase_price=Decimal("50.00"),
        )
        self.assertEqual(ps.last_purchase_price, Decimal("50.00"))

    def test_product_supplier_price_tracking(self):
        ps = ProductSupplier.objects.create(
            product=self.product,
            supplier=self.supplier,
            last_purchase_price=Decimal("75.50"),
        )
        ps.last_purchase_price = Decimal("70.00")
        ps.save()
        self.assertEqual(
            ProductSupplier.objects.get(pk=ps.pk).last_purchase_price,
            Decimal("70.00"),
        )

    def test_multiple_suppliers_per_product(self):
        supplier2 = Supplier.objects.create(
            name="Supplier2", phone="+375292222222", email="s2@test.com", address="Addr2"
        )
        ProductSupplier.objects.create(
            product=self.product, supplier=self.supplier, last_purchase_price=Decimal("50")
        )
        ProductSupplier.objects.create(
            product=self.product,
            supplier=supplier2,
            last_purchase_price=Decimal("45"),
        )
        self.assertEqual(ProductSupplier.objects.filter(product=self.product).count(), 2)

    def test_product_supplier_soft_delete(self):
        ps = ProductSupplier.objects.create(
            product=self.product,
            supplier=self.supplier,
            last_purchase_price=Decimal("50"),
        )
        ps.soft_delete()
        self.assertTrue(ps.is_deleted)
