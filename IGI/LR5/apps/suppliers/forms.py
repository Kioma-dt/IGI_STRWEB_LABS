from __future__ import annotations

from django import forms

from apps.suppliers.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "phone", "email", "address", "is_active")
        labels = {
            "name": "Название поставщика",
            "phone": "Телефон",
            "email": "E-mail",
            "address": "Адрес",
            "is_active": "Активен",
        }
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }