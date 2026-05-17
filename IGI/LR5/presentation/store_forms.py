from __future__ import annotations

import django_filters
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

from application.services.shop_staff_services import apply_icontains_q
from apps.catalog.models import Category, Product
from apps.reviews.models import Review
from apps.suppliers.models import Supplier
from apps.users.constants import GROUP_CUSTOMER, GROUP_EMPLOYEE
from apps.users.models import CustomerProfile, EmployeeProfile
from core.validators import validate_phone_by_format_375_29, validate_age_18_plus


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        label="Количество",
        min_value=1,
        max_value=99,
        initial=1,
    )


class StoreProductFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_q", label="Поиск")
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_deleted=False).order_by("name"),
        empty_label="Все категории",
        null_label="Без категории",
        label="Категория",
    )
    min_price = django_filters.NumberFilter(
        field_name="base_price",
        lookup_expr="gte",
        label="Цена от",
    )
    max_price = django_filters.NumberFilter(
        field_name="base_price",
        lookup_expr="lte",
        label="Цена до",
    )

    class Meta:
        model = Product
        fields = ("category",)

    def filter_q(self, queryset, name, value):
        return apply_icontains_q(queryset, value, "name", "sku", "description")

    @property
    def qs(self):
        qs = super().qs
        # If stale/invalid category is passed via query string, ignore it silently.
        if not self.form.is_valid() and "category" in self.form.errors:
            return self.queryset
        return qs


class StoreReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "title", "body")
        widgets = {
            "body": forms.Textarea(attrs={"rows": 5, "cols": 60}),
            "title": forms.TextInput(attrs={"size": 40}),
        }

    def clean_rating(self) -> int:
        r = int(self.cleaned_data["rating"])
        if r < 1 or r > 5:
            raise forms.ValidationError("Оценка от 1 до 5.")
        return r


class ContactMessageForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        max_length=120,
    )
    email = forms.EmailField(label="E-mail", validators=[EmailValidator()])
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={"rows": 6, "cols": 60}),
        min_length=10,
        max_length=4000,
    )


class VacancyApplicationForm(forms.Form):
    applicant_name = forms.CharField(label="ФИО", max_length=255)
    email = forms.EmailField(label="E-mail")
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    cover_letter = forms.CharField(
        label="Сопроводительное письмо",
        widget=forms.Textarea(attrs={"rows": 8, "cols": 60}),
        min_length=20,
        max_length=8000,
    )


class CheckoutForm(forms.Form):
    promo_code = forms.CharField(
        label="Промокод (необязательно)",
        max_length=32,
        required=False,
    )


class CustomerSignupForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)
    full_name = forms.CharField(label="Полное имя", max_length=255)
    phone = forms.CharField(
        label="Телефон (формат +375 (29) XXX-XX-XX)",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    birth_date = forms.DateField(
        label="Дата рождения",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            attrs={"type": "date"}
        ),
        validators=[validate_age_18_plus],
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_phone(self) -> str:
        phone = self.cleaned_data["phone"]
        if CustomerProfile.objects.filter(phone=phone, is_deleted=False).exists():
            raise forms.ValidationError("Этот телефон уже зарегистрирован.")
        return phone

    def save(self, commit: bool = True) -> User:  # type: ignore[override]
        from django.db import transaction

        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            with transaction.atomic():
                user.save()
                customer_group, _ = Group.objects.get_or_create(name=GROUP_CUSTOMER)
                user.groups.add(customer_group)
                CustomerProfile.objects.create(
                    user=user,
                    full_name=self.cleaned_data["full_name"],
                    phone=self.cleaned_data["phone"],
                    birth_date=self.cleaned_data["birth_date"]
                )
        return user


class EmployeeSignupForm(UserCreationForm):
    email = forms.EmailField(label="E-mail", required=True)
    full_name = forms.CharField(label="Полное имя", max_length=255)
    phone = forms.CharField(
        label="Телефон (формат +375 (29) XXX-XX-XX)",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    birth_date = forms.DateField(
        label="Дата рождения",
        input_formats=["%d/%m/%Y"],
        widget=forms.DateInput(
            attrs={"type": "date"}
        ),
        validators=[validate_age_18_plus],
    )
    position = forms.CharField(label="Должность", max_length=128)
    suppliers = forms.ModelMultipleChoiceField(
        label="Поставщики, с которыми работаете",
        queryset=Supplier.objects.filter(is_deleted=False, is_active=True).order_by("name"),
        required=False,
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_phone(self) -> str:
        phone = self.cleaned_data["phone"]
        if EmployeeProfile.objects.filter(phone=phone, is_deleted=False).exists():
            raise forms.ValidationError("Этот телефон уже зарегистрирован.")
        return phone

    def save(self, commit: bool = True) -> User:  # type: ignore[override]
        from django.db import transaction

        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            with transaction.atomic():
                user.save()
                profile = EmployeeProfile.objects.create(
                    user=user,
                    full_name=self.cleaned_data["full_name"],
                    phone=self.cleaned_data["phone"],
                    position=self.cleaned_data["position"],
                    birth_date=self.cleaned_data["birth_date"]
                )
                profile.suppliers.set(self.cleaned_data.get("suppliers") or [])
                employee_group, _ = Group.objects.get_or_create(name=GROUP_EMPLOYEE)
                user.groups.add(employee_group)
        return user
