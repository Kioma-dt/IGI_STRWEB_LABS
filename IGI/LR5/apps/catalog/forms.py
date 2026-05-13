from __future__ import annotations

from django import forms

from apps.catalog.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "parent", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self) -> dict:
        data = super().clean()
        parent = data.get("parent")
        if self.instance.pk and parent and parent.pk == self.instance.pk:
            raise forms.ValidationError("A category cannot be its own parent.")
        return data


class ProductCreateForm(forms.ModelForm):
    initial_stock = forms.IntegerField(
        label="Initial stock quantity",
        min_value=0,
        initial=0,
        required=False,
    )

    class Meta:
        model = Product
        fields = (
            "name",
            "sku",
            "category",
            "description",
            "image",
            "base_price",
            "age_restriction",
            "is_active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "sku",
            "category",
            "description",
            "image",
            "base_price",
            "age_restriction",
            "is_active",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
