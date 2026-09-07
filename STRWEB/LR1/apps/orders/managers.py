from __future__ import annotations

from django.db import models

from apps.orders.querysets import OrderQuerySet


class OrderManager(models.Manager["Order"]):
    def get_queryset(self) -> OrderQuerySet:
        return OrderQuerySet(self.model, using=self._db)
