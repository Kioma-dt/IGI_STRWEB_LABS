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
        EMPLOYEE = "employee", "employee"

    type = models.CharField(
        "type",
        max_length=16,
        choices=ContactType.choices,
    )
    value = models.CharField("value", max_length=255)
    is_primary = models.BooleanField("primary", default=False)
    photo = models.ImageField(
        "employee photo",
        upload_to="staff_photos/%Y/%m/",
        null=True,
        blank=True,
    )
    employee_name = models.CharField("employee name", max_length=255, blank=True)
    job_description = models.TextField("job description", blank=True)
    phone_number = models.CharField("phone number", max_length=20, blank=True)
    email_address = models.EmailField("email address", blank=True)

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
        if self.employee_name:
            return self.employee_name
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
    logo = models.ImageField(
        "logo",
        upload_to="company/",
        null=True,
        blank=True,
    )
    video = models.FileField(
        "company video",
        upload_to="company/videos/",
        null=True,
        blank=True,
        help_text="Локальный видеоролик о компании (mp4).",
    )
    audio = models.FileField(
        "company audio",
        upload_to="company/audio/",
        null=True,
        blank=True,
        help_text="Локальный аудиофайл (например приветствие).",
    )
    video_url = models.URLField(
        "video URL (устаревшее)",
        blank=True,
        help_text="Не использовать для встраивания; предпочтителен FileField video.",
    )
    certificate_image = models.ImageField(
        "certificate image",
        upload_to="company/",
        null=True,
        blank=True,
    )
    requisites = models.TextField("requisites", blank=True)
    certificate_text = models.TextField("certificate text", blank=True)
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


class CompanyHistoryEntry(SoftDeleteModel):
    company = models.ForeignKey(
        CompanyInfo,
        on_delete=models.CASCADE,
        related_name="history_entries",
        verbose_name="company",
    )
    year = models.PositiveIntegerField("year")
    description = models.TextField("description")

    class Meta:
        verbose_name = "company history entry"
        verbose_name_plural = "company history entries"
        ordering = ["year"]
        indexes = [
            models.Index(fields=["year"], name="company_history_year_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.year}: {self.company_id}"


class Partner(SoftDeleteModel):
    name = models.CharField("name", max_length=255)
    logo = models.ImageField(
        "logo",
        upload_to="partners/",
        null=True,
        blank=True,
    )
    url = models.URLField("website URL")
    is_active = models.BooleanField("active", default=True)
    sort_order = models.PositiveIntegerField("sort order", default=0)

    class Meta:
        verbose_name = "partner"
        verbose_name_plural = "partners"
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=["is_active"], name="partner_active_idx"),
            models.Index(fields=["sort_order"], name="partner_sort_idx"),
        ]

    def __str__(self) -> str:
        return self.name


class Banner(SoftDeleteModel):
    title = models.CharField("title", max_length=255)
    image = models.ImageField(
        "image",
        upload_to="banners/",
        null=True,
        blank=True,
    )
    link_url = models.URLField("link URL", blank=True)
    is_active = models.BooleanField("active", default=True)
    sort_order = models.PositiveIntegerField("sort order", default=0)

    class Meta:
        verbose_name = "banner"
        verbose_name_plural = "banners"
        ordering = ["sort_order", "title"]
        indexes = [
            models.Index(fields=["is_active"], name="banner_active_idx"),
        ]

    def __str__(self) -> str:
        return self.title


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
