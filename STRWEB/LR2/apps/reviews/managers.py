from __future__ import annotations

from django.db import models

from apps.reviews.querysets import ReviewQuerySet


class ReviewManager(models.Manager["Review"]):
    def get_queryset(self) -> ReviewQuerySet:
        return ReviewQuerySet(self.model, using=self._db)
