from __future__ import annotations

from decimal import Decimal

from rest_framework import serializers

from apps.catalog.models import Product


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "base_price", "is_active")


class ProductSetPriceSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    new_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal("0"))
