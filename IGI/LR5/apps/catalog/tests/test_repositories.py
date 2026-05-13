from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.catalog.models import Category, Product
from apps.catalog.repositories import CategoryRepository, ProductRepository
from apps.news.repositories import NewsArticleRepository
from apps.orders.models import Order
from apps.orders.repositories import OrderRepository
from apps.promotions.models import PromoCode
from apps.promotions.repositories import PromoCodeRepository
from apps.reviews.models import Review
from apps.reviews.repositories import ReviewRepository
from apps.suppliers.models import Supplier
from apps.suppliers.repositories import SupplierRepository
from apps.users.models import CustomerProfile

User = get_user_model()


def _phone(suffix: str) -> str:
    return f"+375 (29) {suffix[:3]}-{suffix[3:5]}-{suffix[5:7]}"


class RepositoryLayerTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="cust1",
            email="cust1@example.com",
            password="x" * 12,
        )
        self.customer = CustomerProfile.objects.create(
            user=self.user,
            full_name="Jane Customer",
            birth_date=date(1990, 1, 1),
            phone=_phone("1111111"),
        )
        self.category = Category.objects.create(
            name="Food",
            slug="food",
            parent=None,
        )
        self.product_a = Product.objects.create(
            name="Dog Food Premium",
            sku="SKU-A",
            category=self.category,
            base_price=Decimal("25.00"),
        )
        self.product_b = Product.objects.create(
            name="Cat Snack",
            sku="SKU-B",
            category=self.category,
            base_price=Decimal("10.00"),
        )
        self.supplier = Supplier.objects.create(
            name="Supply Co",
            phone=_phone("2222222"),
        )

    def test_product_repository_search_and_price_filter(self) -> None:
        repo = ProductRepository()
        page = repo.search("Dog", page=1, page_size=10)
        self.assertEqual(page.total_count, 1)
        self.assertEqual(page.items[0].sku, "SKU-A")

        price_page = repo.filter_by_price(
            min_price=Decimal("15.00"),
            max_price=Decimal("30.00"),
            page=1,
            page_size=10,
        )
        self.assertEqual(price_page.total_count, 1)
        self.assertEqual(price_page.items[0].sku, "SKU-A")

    def test_product_repository_filter_by_category(self) -> None:
        repo = ProductRepository()
        page = repo.filter_by_category(self.category.pk, page=1, page_size=10)
        self.assertEqual(page.total_count, 2)

    def test_product_repository_get_popular_products(self) -> None:
        Review.objects.create(
            product=self.product_a,
            customer=self.customer,
            rating=5,
            title="Great",
            body="Nice",
        )
        Review.objects.create(
            product=self.product_b,
            customer=self.customer,
            rating=2,
            title="Meh",
            body="Ok",
        )
        popular = ProductRepository().get_popular_products(limit=5)
        self.assertGreaterEqual(len(popular), 1)
        self.assertEqual(popular[0].pk, self.product_a.pk)

    def test_category_repository_search(self) -> None:
        page = CategoryRepository().search("Food", page=1, page_size=10)
        self.assertEqual(page.total_count, 1)

    def test_supplier_repository_search(self) -> None:
        page = SupplierRepository().search("Supply", page=1, page_size=10)
        self.assertEqual(page.total_count, 1)

    def test_order_repository_search_by_reference(self) -> None:
        order = Order.objects.create(customer=self.customer)
        page = OrderRepository().search(order.reference_number[:6], page=1, page_size=10)
        self.assertGreaterEqual(page.total_count, 1)

    def test_promo_code_repository_active_and_search(self) -> None:
        today = timezone.localdate()
        PromoCode.objects.create(
            code="SAVE10",
            discount_percent=Decimal("10.00"),
            valid_from=today - timedelta(days=1),
            valid_until=today + timedelta(days=7),
            max_uses=100,
            current_uses=0,
            is_active=True,
        )
        repo = PromoCodeRepository()
        active = repo.get_active_promocodes(on_date=today, page=1, page_size=10)
        self.assertGreaterEqual(active.total_count, 1)
        found = repo.search("SAVE", page=1, page_size=10)
        self.assertGreaterEqual(found.total_count, 1)

    def test_news_article_repository_latest_and_search(self) -> None:
        now = timezone.now()
        NewsArticleRepository().create(
            {
                "title": "Opening",
                "slug": "opening",
                "body": "We are open.",
                "published_at": now,
                "is_published": True,
            },
        )
        repo = NewsArticleRepository()
        latest = repo.get_latest_news(limit=5)
        self.assertGreaterEqual(len(latest), 1)
        page = repo.search("Opening", page=1, page_size=10)
        self.assertGreaterEqual(page.total_count, 1)

    def test_review_repository_search(self) -> None:
        Review.objects.create(
            product=self.product_a,
            customer=self.customer,
            rating=4,
            title="Tasty food",
            body="Dog loves it",
        )
        page = ReviewRepository().search("Tasty", page=1, page_size=10)
        self.assertGreaterEqual(page.total_count, 1)

    def test_soft_delete_via_repository(self) -> None:
        repo = ProductRepository()
        repo.delete(self.product_b)
        self.assertFalse(Product.objects.filter(pk=self.product_b.pk, is_deleted=False).exists())
