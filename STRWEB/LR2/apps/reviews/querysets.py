from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Q, QuerySet

from core.repositories.querysets import SoftDeleteQuerySet

if TYPE_CHECKING:
    from apps.reviews.models import Review


class ReviewQuerySet(SoftDeleteQuerySet["Review"]):
    def active(self) -> QuerySet["Review"]:
        return self.alive().filter(is_published=True)

    def search(self, text: str) -> QuerySet["Review"]:
        return self.active().filter(
            Q(title__icontains=text) | Q(body__icontains=text),
        )
