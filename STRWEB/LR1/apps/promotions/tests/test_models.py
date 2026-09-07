from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta, date

from apps.promotions.models import PromoCode


class PromoCodeModelTest(TestCase):
    """Тесты для модели PromoCode"""

    def test_create_promo_code(self):
        today = date.today()
        promo = PromoCode.objects.create(
            code="PROMO10",
            discount_percent=Decimal("10.00"),
            valid_from=today,
            valid_until=today + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            is_active=True,
        )
        self.assertEqual(promo.code, "PROMO10")
        self.assertEqual(promo.discount_percent, Decimal("10.00"))

    def test_promo_code_case_sensitive(self):
        today = date.today()
        PromoCode.objects.create(
            code="PROMO", valid_from=today, valid_until=today + timedelta(days=1)
        )
        # Можно создать с другим регистром
        promo2 = PromoCode.objects.create(
            code="promo", valid_from=today, valid_until=today + timedelta(days=1)
        )
        self.assertEqual(promo2.code, "promo")

    def test_promo_code_inactive(self):
        today = date.today()
        promo = PromoCode.objects.create(
            code="INACTIVE",
            valid_from=today,
            valid_until=today + timedelta(days=1),
            is_active=False,
        )
        self.assertFalse(promo.is_active)

    def test_promo_code_uses_tracking(self):
        today = date.today()
        promo = PromoCode.objects.create(
            code="TRACK",
            valid_from=today,
            valid_until=today + timedelta(days=1),
            max_uses=5,
            current_uses=0,
        )
        self.assertEqual(promo.current_uses, 0)
        self.assertEqual(promo.max_uses, 5)

    def test_promo_code_discount_percent(self):
        today = date.today()
        discounts = [Decimal("5"), Decimal("15.5"), Decimal("50")]
        for discount in discounts:
            promo = PromoCode.objects.create(
                code=f"PROMO{discount}",
                discount_percent=discount,
                valid_from=today,
                valid_until=today + timedelta(days=1),
            )
            self.assertEqual(promo.discount_percent, discount)

    def test_promo_code_soft_delete(self):
        today = date.today()
        promo = PromoCode.objects.create(
            code="DELETE",
            valid_from=today,
            valid_until=today + timedelta(days=1),
        )
        promo.soft_delete()
        self.assertTrue(promo.is_deleted)
