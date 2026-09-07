from __future__ import annotations

from dataclasses import dataclass

from core.exceptions import BusinessValidationError

_ALLOWED_ROLES = frozenset({"customer", "employee", "admin"})


@dataclass(frozen=True)
class AssignRoleDTO:
    user_id: int
    role_name: str
    replace_existing: bool = False

    def __post_init__(self) -> None:
        if self.user_id < 1:
            raise BusinessValidationError("user_id must be positive.")
        name = self.role_name.strip().lower()
        if name not in _ALLOWED_ROLES:
            raise BusinessValidationError(
                f"Unsupported role '{self.role_name}'. Allowed: {sorted(_ALLOWED_ROLES)}.",
            )
        object.__setattr__(self, "role_name", name)


@dataclass(frozen=True)
class RemoveRoleDTO:
    user_id: int
    role_name: str

    def __post_init__(self) -> None:
        if self.user_id < 1:
            raise BusinessValidationError("user_id must be positive.")
        name = self.role_name.strip().lower()
        if name not in _ALLOWED_ROLES:
            raise BusinessValidationError(
                f"Unsupported role '{self.role_name}'. Allowed: {sorted(_ALLOWED_ROLES)}.",
            )
        object.__setattr__(self, "role_name", name)
