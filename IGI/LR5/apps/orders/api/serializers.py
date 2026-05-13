from __future__ import annotations

from rest_framework import serializers


class OrderLineInputSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)


class PlaceOrderRequestSerializer(serializers.Serializer):
    lines = OrderLineInputSerializer(many=True)
    promo_code = serializers.CharField(required=False, allow_blank=True, default="")

    def validate_lines(self, value: list) -> list:
        if not value:
            raise serializers.ValidationError("At least one line is required.")
        return value
