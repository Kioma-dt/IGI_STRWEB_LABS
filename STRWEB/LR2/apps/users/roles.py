from __future__ import annotations

from typing import Any

from apps.users.constants import GROUP_ADMIN, GROUP_CUSTOMER, GROUP_EMPLOYEE


def is_authenticated(user: Any) -> bool:
    return bool(getattr(user, "is_authenticated", False))


def is_in_group(user: Any, group_name: str) -> bool:
    if not is_authenticated(user):
        return False
    return user.groups.filter(name=group_name).exists()


def is_super_admin(user: Any) -> bool:
    return bool(is_authenticated(user) and getattr(user, "is_superuser", False))


def is_admin(user: Any) -> bool:
    return is_super_admin(user) or is_in_group(user, GROUP_ADMIN)


def is_employee(user: Any) -> bool:
    if not is_authenticated(user):
        return False
    if is_admin(user) or getattr(user, "is_staff", False):
        return True
    return is_in_group(user, GROUP_EMPLOYEE)


def is_customer(user: Any) -> bool:
    if not is_authenticated(user):
        return False
    if is_in_group(user, GROUP_CUSTOMER):
        return True
    profile = getattr(user, "customer_profile", None)
    return bool(profile is not None and not getattr(profile, "is_deleted", True))


def is_employee_limited(user: Any) -> bool:
    """Employee group member without admin elevation."""
    return is_in_group(user, GROUP_EMPLOYEE) and not is_admin(user)

