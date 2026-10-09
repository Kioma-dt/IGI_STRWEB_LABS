from __future__ import annotations

from django.db import models

from apps.promotions.managers import PromoCodeManager
from core.models import SoftDeleteModel


class PromoCode(SoftDeleteModel):
    code = models.CharField("code", max_length=32, unique=True)
    discount_percent = models.DecimalField(
        "discount percent",
        max_digits=5,
        decimal_places=2,
    )
    valid_from = models.DateField("valid from")
    valid_until = models.DateField("valid until", null=True, blank=True)
    max_uses = models.PositiveIntegerField(
        "max uses",
        null=True,
        blank=True,
    )
    current_uses = models.PositiveIntegerField("current uses", default=0)
    is_active = models.BooleanField("active", default=True)
    customers = models.ManyToManyField(
        "users.CustomerProfile",
        related_name="promo_codes",
        blank=True,
        verbose_name="eligible customers",
    )

    objects = PromoCodeManager()

    class Meta:
        verbose_name = "promo code"
        verbose_name_plural = "promo codes"
        indexes = [
            models.Index(fields=["code"], name="promocode_code_idx"),
            models.Index(fields=["is_active"], name="promocode_active_idx"),
            models.Index(
                fields=["valid_from", "valid_until"],
                name="promocode_valid_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.code
