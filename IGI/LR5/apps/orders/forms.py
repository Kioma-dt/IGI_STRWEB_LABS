from __future__ import annotations

from django import forms

from apps.orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "customer",
            "created_by",
            "promo_code",
            "status",
            "total_amount",
        )
        labels = {
            "customer": "Клиент",
            "created_by": "Создан сотрудником",
            "promo_code": "Промокод",
            "status": "Статус заказа",
            "total_amount": "Сумма заказа",
        }
        widgets = {
            "total_amount": forms.NumberInput(attrs={"step": "0.01"}),
        }

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("customer", "created_by", "promo_code", "status", "total_amount")
        labels = {
            "customer": "Клиент",
            "created_by": "Создан сотрудником",
            "promo_code": "Промокод",
            "status": "Статус заказа",
            "total_amount": "Сумма заказа",
        }
        widgets = {
            "total_amount": forms.NumberInput(attrs={"step": "0.01"}),
        }