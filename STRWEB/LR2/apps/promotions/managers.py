from __future__ import annotations

from datetime import date

from django.db import models
from django.db.models import QuerySet

from apps.promotions.querysets import PromoCodeQuerySet


class PromoCodeManager(models.Manager["PromoCode"]):
    def get_queryset(self) -> PromoCodeQuerySet:
        return PromoCodeQuerySet(self.model, using=self._db)

    def active_on(self, on_date: date) -> QuerySet:
        """Get promo codes active on the given date."""
        return self.get_queryset().active_on(on_date)

