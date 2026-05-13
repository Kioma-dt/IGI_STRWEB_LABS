from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Review:
    id: UUID
    product_id: UUID
    customer_id: UUID
    rating: int
    title: str
    body: str
    is_published: bool


@dataclass(frozen=True)
class NewsArticle:
    id: UUID
    title: str
    slug: str
    published_at: datetime | None
    is_published: bool


@dataclass(frozen=True)
class FAQ:
    id: UUID
    question: str
    answer: str
    sort_order: int


@dataclass(frozen=True)
class Vacancy:
    id: UUID
    title: str
    description: str
    is_active: bool
    published_at: datetime | None


@dataclass(frozen=True)
class Contact:
    id: UUID
    type: str
    value: str
    is_primary: bool


@dataclass(frozen=True)
class CompanyInfo:
    id: UUID
    name: str
    legal_address: str
    about: str
    support_email: str
    phone: str
    is_current: bool
