from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

EntityT = TypeVar("EntityT")


class BaseRepository(ABC, Generic[EntityT]):
    @abstractmethod
    def get_by_id(self, entity_id: Any) -> EntityT | None:
        raise NotImplementedError

    @abstractmethod
    def save(self, entity: EntityT) -> EntityT:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: EntityT) -> None:
        raise NotImplementedError
