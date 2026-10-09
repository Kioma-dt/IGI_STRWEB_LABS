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


class Purchase(SoftDeleteModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier",
        on_delete=models.PROTECT,
        related_name="purchases",
        verbose_name="supplier",
    )
    created_by = models.ForeignKey(
        "users.EmployeeProfile",
        on_delete=models.SET_NULL,
        related_name="created_purchases",
        null=True,
        blank=True,
        verbose_name="created by",
    )
    ordered_at = models.DateTimeField("ordered at", auto_now_add=True)
    delivered_at = models.DateTimeField(
        "delivered at",
        null=True,
        blank=True,
    )
    reference_number = models.CharField(
        "reference number",
        max_length=64,
        unique=True,
        db_index=True,
        default=_generate_order_reference,
        editable=False,
    )

    class Meta:
        verbose_name = "purchase"
        verbose_name_plural = "purchases"
        indexes = [
            models.Index(
                fields=["supplier", "ordered_at"],
                name="purchase_supplier_ordered_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.reference_number


class PurchaseItem(SoftDeleteModel):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="purchase",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="purchase_items",
        verbose_name="product",
    )
    quantity = models.PositiveIntegerField("quantity")
    purchase_price = models.DecimalField(
        "purchase price",
        max_digits=10,
        decimal_places=2,
        help_text="Unit purchase price for this inbound shipment line.",
    )

    class Meta:
        verbose_name = "purchase item"
        verbose_name_plural = "purchase items"
        constraints = [
            models.UniqueConstraint(
                fields=["purchase", "product"],
                name="uniq_purchase_product_item",
            ),
        ]
        indexes = [
            models.Index(fields=["purchase"], name="purchaseitem_purchase_idx"),
            models.Index(fields=["product"], name="purchaseitem_product_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.purchase_id} x {self.product_id} ({self.quantity})"


class OrderItem(SoftDeleteModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="order",
    )
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="product",
    )
    quantity = models.PositiveIntegerField("quantity")
    unit_price = models.DecimalField(
        "unit price",
        max_digits=10,
        decimal_places=2,
    )
    line_total = models.DecimalField(
        "line total",
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        verbose_name = "order item"
        verbose_name_plural = "order items"
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="uniq_order_product_item",
            ),
        ]
        indexes = [
            models.Index(fields=["order"], name="orderitem_order_idx"),
            models.Index(fields=["product"], name="orderitem_product_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.order_id} x {self.product_id} ({self.quantity})"
