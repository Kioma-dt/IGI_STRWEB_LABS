from __future__ import annotations

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction

from application.dto.user import AssignRoleDTO, RemoveRoleDTO
from core.exceptions import RoleManagementError, UserNotFoundError

User = get_user_model()

logger = logging.getLogger(__name__)

_ROLE_NAMES = ("customer", "employee", "admin")


class UserService:
    """Django auth Group-based role management (no HTTP)."""

    @staticmethod
    def ensure_default_groups() -> None:
        for name in _ROLE_NAMES:
            Group.objects.get_or_create(name=name)

    @transaction.atomic
    def assign_role(self, payload: AssignRoleDTO) -> None:
        self.ensure_default_groups()
        user = (
            User.objects.select_for_update()
            .filter(pk=payload.user_id, is_active=True)
            .first()
        )
        if user is None:
            logger.warning("User not found for role assignment: %s", payload.user_id)
            raise UserNotFoundError("User not found or inactive.")

        try:
            group = Group.objects.get(name=payload.role_name)
        except Group.DoesNotExist as exc:
            raise RoleManagementError("Role group missing.") from exc

        if payload.replace_existing:
            user.groups.clear()
        user.groups.add(group)
        logger.info("Assigned role %s to user %s", payload.role_name, payload.user_id)

    @transaction.atomic
    def remove_role(self, payload: RemoveRoleDTO) -> None:
        self.ensure_default_groups()
        user = User.objects.filter(pk=payload.user_id).first()
        if user is None:
            raise UserNotFoundError("User not found.")
        try:
            group = Group.objects.get(name=payload.role_name)
        except Group.DoesNotExist as exc:
            raise RoleManagementError("Role group missing.") from exc
        user.groups.remove(group)
        logger.info("Removed role %s from user %s", payload.role_name, payload.user_id)
