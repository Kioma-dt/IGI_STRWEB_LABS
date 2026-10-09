from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.orders.models import Order


class OrderQuerySet(SoftDeleteQuerySet["Order"]):
    def active(self) -> QuerySet["Order"]:
        return self.alive()

    def search(self, text: str) -> QuerySet["Order"]:
        return self.active().filter(
            Q(reference_number__icontains=text)
            | Q(status__icontains=text)
            | Q(customer__full_name__icontains=text),
        )
