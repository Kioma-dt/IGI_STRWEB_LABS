from __future__ import annotations

import uuid
from decimal import Decimal

from django.db import models

from apps.orders.managers import OrderManager
from core.models import SoftDeleteModel


def _generate_order_reference() -> str:
    return str(uuid.uuid4())


class Order(SoftDeleteModel):
    class Status(models.TextChoices):
        NEW = "new", "new"
        PAID = "paid", "paid"
        SHIPPED = "shipped", "shipped"
        COMPLETED = "completed", "completed"
        CANCELLED = "cancelled", "cancelled"

    reference_number = models.CharField(
        "reference number",
        max_length=64,
        unique=True,
        db_index=True,
        default=_generate_order_reference,
        editable=False,
    )
    customer = models.ForeignKey(
        "users.CustomerProfile",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="customer",
    )
    created_by = models.ForeignKey(
        "users.EmployeeProfile",
        on_delete=models.SET_NULL,
        related_name="created_orders",
        null=True,
        blank=True,
        verbose_name="created by",
    )
    promo_code = models.ForeignKey(
        "promotions.PromoCode",
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
        verbose_name="promo code",
    )
    status = models.CharField(
        "status",
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
    )
    ordered_at = models.DateTimeField("ordered at", auto_now_add=True)
    total_amount = models.DecimalField(
        "total amount",
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    objects = OrderManager()

    class Meta:
        verbose_name = "order"
        verbose_name_plural = "orders"
        indexes = [
            models.Index(fields=["status"], name="order_status_idx"),
            models.Index(fields=["customer"], name="order_customer_idx"),
            models.Index(fields=["ordered_at"], name="order_ordered_at_idx"),
        ]

    def __str__(self) -> str:
        return self.reference_number
