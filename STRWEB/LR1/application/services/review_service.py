from __future__ import annotations

import logging

from django.db import IntegrityError, transaction

from application.dto.review import CreateReviewDTO
from apps.catalog.repositories.product_repository import ProductRepository
from apps.reviews.models import Review
from apps.reviews.repositories.review_repository import ReviewRepository
from apps.users.models import CustomerProfile
from core.exceptions import CustomerNotFoundError, ProductNotFoundError, ReviewDuplicateError

logger = logging.getLogger(__name__)


class ReviewService:
    """Customer review creation rules (no HTTP)."""

    def __init__(
        self,
        *,
        reviews: ReviewRepository | None = None,
        products: ProductRepository | None = None,
    ) -> None:
        self._reviews = reviews or ReviewRepository()
        self._products = products or ProductRepository()

    @transaction.atomic
    def create_review(self, payload: CreateReviewDTO) -> Review:
        product = self._products.get_by_id(payload.product_id)
        if product is None or not product.is_active or product.is_deleted:
            raise ProductNotFoundError("Product not found or inactive.")

        if not CustomerProfile.objects.filter(
            pk=payload.customer_id,
            is_deleted=False,
        ).exists():
            raise CustomerNotFoundError("Customer not found.")

        try:
            review = self._reviews.create(
                {
                    "product_id": payload.product_id,
                    "customer_id": payload.customer_id,
                    "rating": payload.rating,
                    "title": payload.title,
                    "body": payload.body,
                    "is_published": payload.publish,
                },
            )
        except IntegrityError as exc:
            logger.warning("Duplicate review attempt: %s", exc)
            raise ReviewDuplicateError(
                "A review with this title already exists for the product.",
            ) from exc

        logger.info("Review created id=%s product=%s", review.id, payload.product_id)
        return review
