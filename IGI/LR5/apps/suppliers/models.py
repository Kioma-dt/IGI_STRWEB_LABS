from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.suppliers.managers import SupplierManager
from core.models import SoftDeleteModel
from core.validators import validate_phone_by_format_375_29


class Supplier(SoftDeleteModel):
    name = models.CharField("name", max_length=255)
    phone = models.CharField(
        "phone",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    email = models.EmailField("email", blank=True)
    address = models.CharField("address", max_length=255, blank=True)
    is_active = models.BooleanField("active", default=True)

    objects = SupplierManager()

    class Meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "phone"],
                name="uniq_supplier_name_phone",
            ),
        ]
        indexes = [
            models.Index(fields=["name"], name="supplier_name_idx"),
            models.Index(fields=["is_active"], name="supplier_active_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class ProductSupplier(SoftDeleteModel):
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="supplier_links",
        verbose_name="product",
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="product_links",
        verbose_name="supplier",
    )
    last_purchase_price = models.DecimalField(
        "last purchase price",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    class Meta:
        verbose_name = "product supplier link"
        verbose_name_plural = "product supplier links"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "supplier"],
                name="uniq_product_supplier",
            ),
        ]
        indexes = [
            models.Index(
                fields=["product", "supplier"],
                name="product_supplier_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product_id} — {self.supplier_id}"
