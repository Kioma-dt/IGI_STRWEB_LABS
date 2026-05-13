from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.suppliers.models import Supplier


class SupplierQuerySet(SoftDeleteQuerySet["Supplier"]):
    def active(self) -> QuerySet["Supplier"]:
        return self.alive().filter(is_active=True)

    def search(self, text: str) -> QuerySet["Supplier"]:
        return self.active().filter(
            Q(name__icontains=text) | Q(phone__icontains=text),
        )
