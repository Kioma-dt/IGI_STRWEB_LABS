from __future__ import annotations

from django import forms

from apps.suppliers.models import Supplier
from django.forms import inlineformset_factory

from apps.catalog.models import Product
from apps.suppliers.models import ProductSupplier

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

class ProductSupplierForm(forms.ModelForm):
    class Meta:
        model = ProductSupplier
        fields = ("product", "last_purchase_price")
        labels = {
            "product": "Товар",
            "last_purchase_price": "Цена поставки",
        }


class AddToCartForm(forms.Form):
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.none(),
        label="Поставщик",
        empty_label=None,
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label="Количество",
    )


ProductSupplierFormSet = inlineformset_factory(
    parent_model=Supplier,
    model=ProductSupplier,
    form=ProductSupplierForm,
    extra=5,
    can_delete=True,
)
