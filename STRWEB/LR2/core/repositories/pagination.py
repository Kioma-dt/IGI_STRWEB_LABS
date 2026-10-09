from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, Iterable, Protocol, Sequence, TypeVar

T = TypeVar("T")


class CountableSlicable(Protocol[T]):
    def count(self) -> int: ...

    def __getitem__(self, item: slice) -> Sequence[T]: ...

    def __iter__(self) -> Iterable[T]: ...


@dataclass(frozen=True)
class RepositoryPage(Generic[T]):
    items: list[T]
    total_count: int
    page: int
    page_size: int


def paginate_queryset(
    qs: CountableSlicable[T],
    page: int,
    page_size: int,
) -> RepositoryPage[T]:
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")

    total = qs.count()
    offset = (page - 1) * page_size
    limit = offset + page_size

    items = list(qs[offset:limit])
    return RepositoryPage(
        items=items,
        total_count=total,
        page=page,
        page_size=page_size,
    )
