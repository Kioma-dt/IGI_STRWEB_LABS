from __future__ import annotations

from django.db import models

from apps.promotions.querysets import PromoCodeQuerySet


class PromoCodeManager(models.Manager["PromoCode"]):
    def get_queryset(self) -> PromoCodeQuerySet:
        return PromoCodeQuerySet(self.model, using=self._db)
