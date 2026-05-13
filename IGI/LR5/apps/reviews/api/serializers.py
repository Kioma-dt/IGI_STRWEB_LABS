from __future__ import annotations

from rest_framework import serializers


class ReviewCreateSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(required=False, allow_blank=True, default="")
