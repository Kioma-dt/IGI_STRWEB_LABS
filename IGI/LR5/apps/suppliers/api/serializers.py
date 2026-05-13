from __future__ import annotations

from rest_framework import serializers

from apps.suppliers.models import Supplier


class SupplierReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ("id", "name", "phone")
