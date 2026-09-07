from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.catalog.managers import CategoryManager, ProductManager
from core.models import SoftDeleteModel


class Category(SoftDeleteModel):
    name = models.CharField("name", max_length=255)
    slug = models.SlugField("slug", max_length=255)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name="parent category",
    )
    description = models.TextField("description", blank=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "parent"],
                name="uniq_category_slug_parent",
            ),
        ]
        indexes = [
            models.Index(fields=["slug"], name="category_slug_idx"),
            models.Index(fields=["parent"], name="category_parent_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class Product(SoftDeleteModel):
    class AgeRestriction(models.IntegerChoices):
        NONE = 0, "none"
        ADULT_18 = 18, "18+"

    name = models.CharField("name", max_length=255)
    sku = models.CharField("SKU", max_length=64, unique=True)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
        verbose_name="category",
    )
    description = models.TextField("description", blank=True)
    image = models.ImageField(
        "image",
        upload_to="products/",
        blank=True,
        null=True,
    )
    base_price = models.DecimalField(
        "base price",
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    age_restriction = models.IntegerField(
        "age restriction",
        choices=AgeRestriction.choices,
        default=AgeRestriction.NONE,
    )
    is_active = models.BooleanField("active", default=True)
    suppliers = models.ManyToManyField(
        "suppliers.Supplier",
        through="suppliers.ProductSupplier",
        related_name="products",
        verbose_name="suppliers",
    )

    objects = ProductManager()

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        indexes = [
            models.Index(fields=["name"], name="product_name_idx"),
            models.Index(fields=["category"], name="product_category_idx"),
            models.Index(fields=["is_active"], name="product_active_idx"),
            models.Index(fields=["base_price"], name="product_price_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"


class ProductStock(SoftDeleteModel):
    """Physical stock for a product (quantity on hand)."""

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="stock",
        verbose_name="product",
    )
    quantity_on_hand = models.PositiveIntegerField("quantity on hand", default=0)

    class Meta:
        verbose_name = "product stock"
        verbose_name_plural = "product stock"
        indexes = [
            models.Index(fields=["quantity_on_hand"], name="stock_qty_idx"),
        ]

    def __str__(self) -> str:
        return f"Stock({self.product_id})={self.quantity_on_hand}"
