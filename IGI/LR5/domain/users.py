from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class User:
    id: int
    email: str
    is_active: bool


@dataclass(frozen=True)
class CustomerProfile:
    id: UUID
    user_id: int
    full_name: str
    birth_date: date | None
    phone: str
    is_vip: bool


@dataclass(frozen=True)
class EmployeeProfile:
    id: UUID
    user_id: int
    full_name: str
    position: str
    phone: str
    is_active: bool
