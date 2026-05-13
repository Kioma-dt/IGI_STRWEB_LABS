from __future__ import annotations

from django.conf import settings
from django.db import models

from core.models import SoftDeleteModel
from core.validators import validate_age_18_plus, validate_phone_by_format_375_29


class CustomerProfile(SoftDeleteModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        verbose_name="user",
    )
    full_name = models.CharField("full name", max_length=255)
    birth_date = models.DateField(
        "birth date",
        null=True,
        blank=True,
        validators=[validate_age_18_plus],
    )
    phone = models.CharField(
        "phone",
        max_length=20,
        unique=True,
        validators=[validate_phone_by_format_375_29],
    )
    is_vip = models.BooleanField("VIP customer", default=False)

    class Meta:
        verbose_name = "customer profile"
        verbose_name_plural = "customer profiles"
        indexes = [
            models.Index(fields=["phone"], name="customer_phone_idx"),
            models.Index(fields=["is_vip"], name="customer_vip_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.phone})"


class EmployeeProfile(SoftDeleteModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
        verbose_name="user",
    )
    full_name = models.CharField("full name", max_length=255)
    position = models.CharField("position", max_length=128)
    phone = models.CharField(
        "phone",
        max_length=20,
        unique=True,
        validators=[validate_phone_by_format_375_29],
    )
    is_active = models.BooleanField("active", default=True)

    class Meta:
        verbose_name = "employee profile"
        verbose_name_plural = "employee profiles"
        indexes = [
            models.Index(fields=["phone"], name="employee_phone_idx"),
            models.Index(fields=["is_active"], name="employee_active_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.position})"


class ShopPermission(models.Model):
    """
    Permission anchor for RBAC (no business data; Django auth.Permission rows only).
    """

    class Meta:
        default_permissions = ()
        permissions = [
            ("place_order", "Place orders as customer"),
            ("view_own_orders", "View own customer orders"),
            ("view_active_promotions", "View active promotional codes"),
            ("submit_product_review", "Submit product reviews"),
            ("view_suppliers", "View supplier directory"),
            ("view_sales", "View sales information"),
            ("manage_products", "Manage catalog products"),
            ("full_access", "Full administrative access to shop APIs"),
        ]

    def __str__(self) -> str:
        return "ShopPermission"
