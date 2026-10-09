from __future__ import annotations

from django.db import models

from apps.catalog.querysets import CategoryQuerySet, ProductQuerySet


class CategoryManager(models.Manager["Category"]):
    def get_queryset(self) -> CategoryQuerySet:
        return CategoryQuerySet(self.model, using=self._db)


class ProductManager(models.Manager["Product"]):
    def get_queryset(self) -> ProductQuerySet:
        return ProductQuerySet(self.model, using=self._db)
