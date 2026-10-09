from django.test import TestCase
from decimal import Decimal
from datetime import date, timedelta
from unittest.mock import patch

from application.services.promo_code_service import PromoCodeService
from application.dto.promo import ApplyPromoInputDTO, PromoDiscountResultDTO
from apps.promotions.models import PromoCode
from core.exceptions import InvalidPromoCodeError


class PromoCodeServiceTest(TestCase):
    """Тесты для PromoCodeService"""

    def setUp(self):
        self.service = PromoCodeService()
        today = date.today()
        self.valid_promo = PromoCode.objects.create(
            code="VALID10",
            discount_percent=Decimal("10"),
            valid_from=today,
            valid_until=today + timedelta(days=30),
            max_uses=100,
            current_uses=0,
            is_active=True,
        )

    def test_evaluate_discount_valid_code(self):
        dto = ApplyPromoInputDTO(
            code="VALID10", basket_total=Decimal("100.00"), customer_id=1
        )
        result = self.service.evaluate_discount(dto)
        self.assertEqual(result.discount_amount, Decimal("10.00"))
        self.assertEqual(result.final_total, Decimal("90.00"))

    def test_evaluate_discount_invalid_code(self):
        dto = ApplyPromoInputDTO(
            code="INVALID", basket_total=Decimal("100"), customer_id=1
        )
        with self.assertRaises(InvalidPromoCodeError):
            self.service.evaluate_discount(dto)

    def test_evaluate_discount_expired_code(self):
        expired = PromoCode.objects.create(
            code="EXPIRED",
            discount_percent=Decimal("10"),
            valid_from=date.today() - timedelta(days=30),
            valid_until=date.today() - timedelta(days=1),
            is_active=True,
        )
        dto = ApplyPromoInputDTO(code="EXPIRED", basket_total=Decimal("100"), customer_id=1)
        with self.assertRaises(InvalidPromoCodeError):
            self.service.evaluate_discount(dto)

    def test_evaluate_discount_inactive_code(self):
        inactive = PromoCode.objects.create(
            code="INACTIVE",
            discount_percent=Decimal("10"),
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=1),
            is_active=False,
        )
        dto = ApplyPromoInputDTO(code="INACTIVE", basket_total=Decimal("100"), customer_id=1)
        with self.assertRaises(InvalidPromoCodeError):
            self.service.evaluate_discount(dto)

    def test_evaluate_discount_max_uses_exceeded(self):
        maxed = PromoCode.objects.create(
            code="MAXED",
            discount_percent=Decimal("10"),
            valid_from=date.today(),
            valid_until=date.today() + timedelta(days=1),
            max_uses=1,
            current_uses=1,
            is_active=True,
        )
        dto = ApplyPromoInputDTO(code="MAXED", basket_total=Decimal("100"), customer_id=1)
        with self.assertRaises(InvalidPromoCodeError):
            self.service.evaluate_discount(dto)

    def test_register_use(self):
        dto = ApplyPromoInputDTO(
            code="VALID10", basket_total=Decimal("100"), customer_id=1
        )
        result = self.service.evaluate_discount(dto)
        self.service.register_use("VALID10")

        updated = PromoCode.objects.get(code="VALID10")
        self.assertEqual(updated.current_uses, 1)

    def test_discount_calculation_different_amounts(self):
        amounts = [Decimal("50"), Decimal("100"), Decimal("500.50")]
        for amount in amounts:
            dto = ApplyPromoInputDTO(code="VALID10", basket_total=amount, customer_id=1)
            result = self.service.evaluate_discount(dto)
            expected_discount = amount * Decimal("10") / Decimal("100")
            self.assertEqual(result.discount_amount, expected_discount)
