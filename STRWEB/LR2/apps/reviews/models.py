from __future__ import annotations

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.reviews.managers import ReviewManager
from core.models import SoftDeleteModel


class Review(SoftDeleteModel):
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="product",
    )
    customer = models.ForeignKey(
        "users.CustomerProfile",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="customer",
    )
    rating = models.PositiveSmallIntegerField(
        "rating",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    title = models.CharField("title", max_length=255)
    body = models.TextField("body", blank=True)
    is_published = models.BooleanField("published", default=True)

    objects = ReviewManager()

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
        indexes = [
            models.Index(fields=["product"], name="review_product_idx"),
            models.Index(fields=["is_published"], name="review_published_idx"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "customer", "title"],
                name="uniq_review_product_customer_title",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.product_id} — {self.rating}"
