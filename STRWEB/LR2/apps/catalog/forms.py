from __future__ import annotations

from django import forms

from apps.catalog.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "parent", "description")
        labels = {
            "name": "Название",
            "slug": "URL-адрес (slug)",
            "parent": "Родительская категория",
            "description": "Описание",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self) -> dict:
        data = super().clean()
        parent = data.get("parent")
        if self.instance.pk and parent and parent.pk == self.instance.pk:
            raise forms.ValidationError("Категория не может быть родительской сама себе.")
        return data


class ProductCreateForm(forms.ModelForm):
    initial_stock = forms.IntegerField(
        label="Начльное количество на складе",
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
        labels = {
            "name": "Название",
            "sku": "Артикул",
            "category": "Категория",
            "description": "Описание",
            "image": "Изображение",
            "base_price": "Цена",
            "age_restriction": "Возрастное ограничение",
            "is_active": "Активен",
        }
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
        labels = {
            "name": "Название",
            "sku": "Артикул",
            "category": "Категория",
            "description": "Описание",
            "image": "Изображение",
            "base_price": "Цена",
            "age_restriction": "Возрастное ограничение",
            "is_active": "Активен",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }