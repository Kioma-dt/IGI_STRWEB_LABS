from django.test import TestCase
from django.utils import timezone
from decimal import Decimal

from apps.reviews.models import Review
from apps.catalog.models import Category, Product
from apps.users.models import CustomerProfile
from django.contrib.auth.models import User


class ReviewModelTest(TestCase):
    """Тесты для модели Review"""

    def setUp(self):
        self.user = User.objects.create_user("user", "u@test.com", "pass")
        self.customer = CustomerProfile.objects.create(user=self.user)

        category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Product", sku="SKU1", category=category, base_price=Decimal("50")
        )

    def test_create_review(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            rating=5,
            title="Great product!",
            body="Really good",
            is_published=True,
        )
        self.assertEqual(review.rating, 5)
        self.assertTrue(review.is_published)

    def test_review_rating_range(self):
        for rating in range(1, 6):
            review = Review.objects.create(
                product=self.product,
                customer=self.customer,
                rating=rating,
                title=f"Rating {rating}",
            )
            self.assertEqual(review.rating, rating)

    def test_review_unpublished(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            rating=3,
            title="Test",
            is_published=False,
        )
        self.assertFalse(review.is_published)

    def test_review_body_optional(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            rating=4,
            title="Title",
            body="",
        )
        self.assertEqual(review.body, "")

    def test_review_soft_delete(self):
        review = Review.objects.create(
            product=self.product,
            customer=self.customer,
            rating=5,
            title="Test",
        )
        review.soft_delete()
        self.assertTrue(review.is_deleted)
