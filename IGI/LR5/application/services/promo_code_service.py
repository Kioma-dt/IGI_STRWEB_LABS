from __future__ import annotations

import logging
from datetime import date
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID

from django.utils import timezone

from application.dto.promo import ApplyPromoInputDTO, PromoDiscountResultDTO
from apps.promotions.models import PromoCode
from apps.promotions.repositories.promo_code_repository import PromoCodeRepository
from core.exceptions import InvalidPromoCodeError

logger = logging.getLogger(__name__)


class PromoCodeService:
    """Promo validation and discount calculation (no HTTP)."""

    def __init__(self, promo_codes: PromoCodeRepository | None = None) -> None:
        self._promos = promo_codes or PromoCodeRepository()

    def evaluate_discount(self, payload: ApplyPromoInputDTO) -> PromoDiscountResultDTO:
        promo = self._promos.get_by_code(payload.promo_code)
        if promo is None:
            logger.info("Promo code not found: %s", payload.promo_code)
            raise InvalidPromoCodeError("Promo code not found.")

        self._assert_promo_active(promo, payload.customer_id, on_date=timezone.localdate())

        discount = self._compute_discount(payload.order_subtotal, promo.discount_percent)
        return PromoDiscountResultDTO(
            promo_id=promo.id,
            promo_code=promo.code,
            discount_amount=discount,
            discount_percent=promo.discount_percent,
        )

    def _assert_promo_active(
        self,
        promo: PromoCode,
        customer_id,
        *,
        on_date: date,
    ) -> None:
        if not promo.is_active or promo.is_deleted:
            raise InvalidPromoCodeError("Promo code is inactive.")
        if promo.valid_from > on_date:
            raise InvalidPromoCodeError("Promo code is not valid yet.")
        if promo.valid_until is not None and promo.valid_until < on_date:
            raise InvalidPromoCodeError("Promo code has expired.")
        if promo.max_uses is not None and promo.current_uses >= promo.max_uses:
            raise InvalidPromoCodeError("Promo code usage limit reached.")

        eligible = promo.customers.filter(pk=customer_id)
        if promo.customers.exists() and not eligible.exists():
            raise InvalidPromoCodeError("Promo code is not eligible for this customer.")

    @staticmethod
    def _compute_discount(subtotal: Decimal, percent: Decimal) -> Decimal:
        raw = subtotal * (percent / Decimal("100"))
        return raw.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def register_use(self, promo_id) -> None:
        from django.db.models import F

        updated = PromoCode.objects.filter(pk=promo_id).update(
            current_uses=F("current_uses") + 1,
        )
        if updated != 1:
            logger.error("Failed to increment promo uses for %s", promo_id)
            raise InvalidPromoCodeError("Could not register promo usage.")

    def get_promo_entity(self, promo_id: UUID | None) -> PromoCode | None:
        if promo_id is None:
            return None
        return self._promos.get_by_id(promo_id)
