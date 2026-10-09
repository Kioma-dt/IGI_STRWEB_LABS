from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from application.dto.orders import OrderLineInputDTO, PlaceOrderDTO
from application.dto.product import RestockProductDTO, SetBasePriceDTO
from application.dto.promo import ApplyPromoInputDTO
from application.dto.review import CreateReviewDTO
from application.dto.supplier import UpdateSupplyPriceDTO
from application.dto.user import AssignRoleDTO
from application.services.order_service import OrderService
from application.services.product_service import ProductService
from application.services.promo_code_service import PromoCodeService
from application.services.review_service import ReviewService
from application.services.statistics_service import StatisticsService
from application.services.supplier_service import SupplierService
from application.services.user_service import UserService
from apps.catalog.models import Category, Product, ProductStock
from apps.promotions.models import PromoCode
from apps.suppliers.models import ProductSupplier, Supplier
from apps.users.models import CustomerProfile
from core.exceptions import InsufficientStockError, InvalidPromoCodeError, ReviewDuplicateError

User = get_user_model()


def _phone(suffix: str) -> str:
    return f"+375 (29) {suffix[:3]}-{suffix[3:5]}-{suffix[5:7]}"


class ApplicationServicesTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="u1",
            email="u1@example.com",
            password="password12345",
        )
        self.customer = CustomerProfile.objects.create(
            user=self.user,
            full_name="Test Customer",
            birth_date=date(1990, 1, 1),
            phone=_phone("1111111"),
        )
        self.category = Category.objects.create(name="C", slug="c", parent=None)
        self.product = Product.objects.create(
            name="P1",
            sku="SKU-SVC-1",
            category=self.category,
            base_price=Decimal("10.00"),
        )
        ProductStock.objects.create(product=self.product, quantity_on_hand=5)
        self.supplier = Supplier.objects.create(
            name="S1",
            phone=_phone("2222222"),
        )
        ProductSupplier.objects.create(
            product=self.product,
            supplier=self.supplier,
            last_purchase_price=Decimal("5.00"),
        )

    def test_product_service_restock_and_check_stock(self) -> None:
        svc = ProductService()
        svc.restock(RestockProductDTO(self.product.id, 5))
        result = svc.check_stock(self.product.id, 8)
        self.assertTrue(result.sufficient)
        self.assertEqual(result.available, 10)

    def test_order_service_place_order_reduces_stock(self) -> None:
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=(OrderLineInputDTO(self.product.id, 2),),
            promo_code=None,
        )
        out = OrderService().place_order(dto)
        self.assertEqual(out.total, Decimal("20.00"))
        stock = ProductStock.objects.get(product=self.product)
        self.assertEqual(stock.quantity_on_hand, 3)

    def test_order_service_preview_totals_with_promo(self) -> None:
        today = timezone.localdate()
        promo = PromoCode.objects.create(
            code="PCT10",
            discount_percent=Decimal("10.00"),
            valid_from=today - timedelta(days=1),
            valid_until=today + timedelta(days=2),
            max_uses=10,
            current_uses=0,
            is_active=True,
        )
        promo.customers.add(self.customer)

        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=(OrderLineInputDTO(self.product.id, 1),),
            promo_code="PCT10",
        )
        preview = OrderService().preview_totals(dto)
        self.assertEqual(preview.subtotal, Decimal("10.00"))
        self.assertEqual(preview.discount, Decimal("1.00"))
        self.assertEqual(preview.total, Decimal("9.00"))

    def test_promo_code_service_evaluate_invalid(self) -> None:
        with self.assertRaises(InvalidPromoCodeError):
            PromoCodeService().evaluate_discount(
                ApplyPromoInputDTO(
                    promo_code="MISSING",
                    customer_id=self.customer.id,
                    order_subtotal=Decimal("50.00"),
                ),
            )

    def test_supplier_service_updates_link_price(self) -> None:
        SupplierService().update_supply_price(
            UpdateSupplyPriceDTO(
                product_id=self.product.id,
                supplier_id=self.supplier.id,
                new_purchase_price=Decimal("7.50"),
            ),
        )
        link = ProductSupplier.objects.get(product=self.product, supplier=self.supplier)
        self.assertEqual(link.last_purchase_price, Decimal("7.50"))

    def test_review_service_create(self) -> None:
        rev = ReviewService().create_review(
            CreateReviewDTO(
                product_id=self.product.id,
                customer_id=self.customer.id,
                rating=5,
                title="Great product",
                body="Works well",
            ),
        )
        self.assertEqual(rev.rating, 5)

    def test_review_service_duplicate_title_raises(self) -> None:
        svc = ReviewService()
        payload = CreateReviewDTO(
            product_id=self.product.id,
            customer_id=self.customer.id,
            rating=4,
            title="Same title",
        )
        svc.create_review(payload)
        with self.assertRaises(ReviewDuplicateError):
            svc.create_review(payload)

    def test_user_service_assign_role(self) -> None:
        svc = UserService()
        svc.assign_role(AssignRoleDTO(user_id=self.user.id, role_name="customer"))
        self.assertTrue(self.user.groups.filter(name="customer").exists())

    def test_statistics_service_returns_dto(self) -> None:
        dto = StatisticsService().get_shop_statistics()
        self.assertGreaterEqual(dto.active_products_count, 1)

    def test_product_service_set_base_price(self) -> None:
        ProductService().set_base_price(
            SetBasePriceDTO(self.product.id, Decimal("12.34")),
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.base_price, Decimal("12.34"))

    def test_order_service_insufficient_stock(self) -> None:
        dto = PlaceOrderDTO(
            customer_id=self.customer.id,
            lines=(OrderLineInputDTO(self.product.id, 999),),
        )
        with self.assertRaises(InsufficientStockError):
            OrderService().place_order(dto)
