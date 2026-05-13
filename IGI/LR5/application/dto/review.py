from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from core.exceptions import BusinessValidationError


@dataclass(frozen=True)
class CreateReviewDTO:
    product_id: UUID
    customer_id: UUID
    rating: int
    title: str
    body: str = ""
    publish: bool = True

    def __post_init__(self) -> None:
        title = self.title.strip()
        if not title:
            raise BusinessValidationError("Review title must not be empty.")
        object.__setattr__(self, "title", title)
        if not (1 <= self.rating <= 5):
            raise BusinessValidationError("Rating must be between 1 and 5.")
