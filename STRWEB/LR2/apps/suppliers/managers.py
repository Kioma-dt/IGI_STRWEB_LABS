from __future__ import annotations

from django.db import models

from apps.suppliers.querysets import SupplierQuerySet


class SupplierManager(models.Manager["Supplier"]):
    def get_queryset(self) -> SupplierQuerySet:
        return SupplierQuerySet(self.model, using=self._db)
