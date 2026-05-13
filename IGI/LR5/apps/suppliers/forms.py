from __future__ import annotations

from django import forms

from apps.suppliers.models import Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "phone", "email", "address", "is_active")
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }
