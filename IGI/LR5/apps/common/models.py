from __future__ import annotations

from django.core.validators import EmailValidator
from django.db import models

from core.models import SoftDeleteModel
from core.validators import validate_phone_by_format_375_29


class FAQ(SoftDeleteModel):
    question = models.CharField("question", max_length=255)
    answer = models.TextField("answer")
    sort_order = models.PositiveIntegerField("sort order", default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ entries"
        ordering = ["sort_order", "created_at"]
        indexes = [
            models.Index(fields=["sort_order"], name="faq_sort_idx"),
        ]

    def __str__(self) -> str:
        return self.question


class Vacancy(SoftDeleteModel):
    title = models.CharField("title", max_length=255)
    description = models.TextField("description")
    is_active = models.BooleanField("active", default=True)
    published_at = models.DateTimeField(
        "published at",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "vacancy"
        verbose_name_plural = "vacancies"
        indexes = [
            models.Index(fields=["is_active"], name="vacancy_active_idx"),
            models.Index(fields=["published_at"], name="vacancy_published_idx"),
        ]

    def __str__(self) -> str:
        return self.title


class Contact(SoftDeleteModel):
    class ContactType(models.TextChoices):
        PHONE = "phone", "phone"
        EMAIL = "email", "email"
        ADDRESS = "address", "address"
        SOCIAL = "social", "social"

    type = models.CharField(
        "type",
        max_length=16,
        choices=ContactType.choices,
    )
    value = models.CharField("value", max_length=255)
    is_primary = models.BooleanField("primary", default=False)

    class Meta:
        verbose_name = "contact"
        verbose_name_plural = "contacts"
        constraints = [
            models.UniqueConstraint(
                fields=["type", "value"],
                name="uniq_contact_type_value",
            ),
        ]
        indexes = [
            models.Index(fields=["type"], name="contact_type_idx"),
            models.Index(fields=["is_primary"], name="contact_primary_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.type}: {self.value}"


class CompanyInfo(SoftDeleteModel):
    name = models.CharField("company name", max_length=255)
    legal_address = models.CharField("legal address", max_length=255)
    about = models.TextField("about", blank=True)
    support_email = models.EmailField(
        "support email",
        validators=[EmailValidator()],
    )
    phone = models.CharField(
        "phone",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    is_current = models.BooleanField("current record", default=True, db_index=True)

    class Meta:
        verbose_name = "company information"
        verbose_name_plural = "company information"
        constraints = [
            models.UniqueConstraint(
                fields=["is_current"],
                condition=models.Q(is_current=True),
                name="uniq_companyinfo_single_current",
            ),
        ]
        indexes = [
            models.Index(fields=["name"], name="companyinfo_name_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class PickupPoint(SoftDeleteModel):
    name = models.CharField("name", max_length=255)
    address = models.CharField("address", max_length=255)
    phone = models.CharField(
        "phone",
        max_length=20,
        validators=[validate_phone_by_format_375_29],
    )
    working_hours = models.CharField("working hours", max_length=255, blank=True)
    is_active = models.BooleanField("active", default=True)

    class Meta:
        verbose_name = "pickup point"
        verbose_name_plural = "pickup points"
        indexes = [
            models.Index(fields=["is_active"], name="pickup_active_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.address}"
