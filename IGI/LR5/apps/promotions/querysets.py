from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q, QuerySet

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.promotions.models import PromoCode


class PromoCodeQuerySet(SoftDeleteQuerySet["PromoCode"]):
    def search(self, text: str) -> QuerySet["PromoCode"]:
        return self.alive().filter(code__icontains=text)

    def active_on(self, on_date: date) -> QuerySet["PromoCode"]:
        qs = self.alive().filter(is_active=True)
        qs = qs.filter(valid_from__lte=on_date)
        qs = qs.filter(Q(valid_until__gte=on_date) | Q(valid_until__isnull=True))
        qs = qs.filter(
            Q(max_uses__isnull=True) | Q(current_uses__lt=models.F("max_uses")),
        )
        return qs
