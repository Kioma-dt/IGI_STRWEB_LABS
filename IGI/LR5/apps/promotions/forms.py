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
        labels = {
            "code": "Код промокода",
            "discount_percent": "Скидка (%)",
            "valid_from": "Действует с",
            "valid_until": "Действует до",
            "max_uses": "Максимум использований",
            "current_uses": "Текущее количество использований",
            "is_active": "Активен",
            "customers": "Доступные клиенты",
        }
        widgets = {
            "valid_from": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "valid_until": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "customers": forms.SelectMultiple(attrs={"size": 8}),
        }