from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Generic, Mapping, TypeVar

from django.db import models

from core.repositories.base import BaseRepository
from core.repositories.pagination import RepositoryPage, paginate_queryset

EntityT = TypeVar("EntityT", bound=models.Model)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DjangoModelRepository(BaseRepository[EntityT], Generic[EntityT]):
    """
    Generic repository encapsulating common ORM access patterns.

    Concrete repositories add domain-specific filtering, search, and
    optimized select_related / prefetch_related chains.
    """

    def __init__(
        self,
        model: type[EntityT],
        queryset_factory: Callable[[], models.QuerySet[EntityT]] | None = None,
    ) -> None:
        self._model = model
        self._queryset_factory = queryset_factory

    def _qs(self) -> models.QuerySet[EntityT]:
        if self._queryset_factory is not None:
            return self._queryset_factory()
        return self._model.objects.all()

    def _alive_qs(
        self, qs: models.QuerySet[EntityT]
    ) -> models.QuerySet[EntityT]:
        if hasattr(qs, "alive"):
            return qs.alive()
        if hasattr(self._model, "is_deleted"):
            return qs.filter(is_deleted=False)
        return qs

    def get_by_id(self, entity_id: Any) -> EntityT | None:
        qs = self._alive_qs(self._qs())
        return qs.filter(pk=entity_id).first()

    def list(
        self,
        page: int,
        page_size: int,
        ordering: str,
        filters: Mapping[str, Any] | None = None,
        select_related: list[str] | None = None,
        prefetch_related: list[str] | None = None,
    ) -> RepositoryPage[EntityT]:
        qs = self._alive_qs(self._qs())

        if select_related:
            qs = qs.select_related(*select_related)
        if prefetch_related:
            qs = qs.prefetch_related(*prefetch_related)
        if filters:
            qs = qs.filter(**filters)

        qs = qs.order_by(ordering)
        return paginate_queryset(qs, page=page, page_size=page_size)

    def create(self, data: Mapping[str, Any]) -> EntityT:
        return self._qs().create(**dict(data))

    def update(self, entity_id: Any, data: Mapping[str, Any]) -> EntityT:
        entity = self.get_by_id(entity_id)
        if entity is None:
            raise ValueError("Entity not found")

        for key, value in data.items():
            setattr(entity, key, value)
        entity.save()
        return entity

    def save(self, entity: EntityT) -> EntityT:
        entity.save()
        return entity

    def delete(self, entity: EntityT) -> None:
        if hasattr(entity, "is_deleted") and hasattr(entity, "deleted_at"):
            entity.is_deleted = True
            entity.deleted_at = _utc_now()
            entity.save(update_fields=["is_deleted", "deleted_at"])
            return
        entity.delete()
