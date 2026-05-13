from __future__ import annotations

from django import forms

from apps.promotions.models import PromoCode


class PromoCodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = (
            "code",
            "discount_percent",
            "valid_from",
            "valid_until",
            "max_uses",
            "current_uses",
            "is_active",
            "customers",
        )
        widgets = {
            "customers": forms.SelectMultiple(attrs={"size": 8}),
        }
