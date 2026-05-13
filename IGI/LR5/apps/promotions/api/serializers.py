from __future__ import annotations

from rest_framework import serializers

from apps.promotions.models import PromoCode


class PromoCodeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = (
            "id",
            "code",
            "discount_percent",
            "valid_from",
            "valid_until",
            "is_active",
        )
