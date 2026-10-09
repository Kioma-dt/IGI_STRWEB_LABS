from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from django.db.models import QuerySet

if TYPE_CHECKING:
    from django.db import models as django_models

T = TypeVar("T", bound="django_models.Model")


class SoftDeleteQuerySet(QuerySet[T]):
    def alive(self) -> QuerySet[T]:
        return self.filter(is_deleted=False)
