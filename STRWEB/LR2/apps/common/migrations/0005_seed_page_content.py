# Generated manually for demo content

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.db import migrations
from django.utils import timezone


def seed_page_content(apps, schema_editor):
    CompanyInfo = apps.get_model("common", "CompanyInfo")
    CompanyHistoryEntry = apps.get_model("common", "CompanyHistoryEntry")
    Partner = apps.get_model("common", "Partner")
    Banner = apps.get_model("common", "Banner")
    Contact = apps.get_model("common", "Contact")
    NewsArticle = apps.get_model("news", "NewsArticle")
    PromoCode = apps.get_model("promotions", "PromoCode")

    company = CompanyInfo.objects.filter(is_deleted=False, is_current=True).first()
    if company is None:
        company = CompanyInfo.objects.create(
            name="ЗооМаркет",
            legal_address="г. Минск, ул. Ленина 15",
            about="Сеть магазинов товаров для животных.",
            support_email="support@zooshop.by",
            phone="+375 (29) 888-88-88",
            is_current=True,
        )

    if not company.video_url:
        company.video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    if not company.requisites:
        company.requisites = (
            "ООО «ЗооМаркет»\n"
            "УНП 123456789\n"
            "р/с BY00UNBS00000000000000000000 в ОАО «Банк»\n"
            "BIC UNBSBY2X"
        )
    if not company.certificate_text:
        company.certificate_text = (
            "Сертификат соответствия на розничную торговлю зоотоварами. "
            "Выдан уполномоченным органом. Действует на территории РБ."
        )
    company.save()

    if not CompanyHistoryEntry.objects.filter(company=company, is_deleted=False).exists():
        CompanyHistoryEntry.objects.bulk_create(
            [
                CompanyHistoryEntry(
                    company=company,
                    year=2018,
                    description="Открытие первого магазина в Минске.",
                ),
                CompanyHistoryEntry(
                    company=company,
                    year=2020,
                    description="Запуск интернет-витрины и доставки.",
                ),
                CompanyHistoryEntry(
                    company=company,
                    year=2023,
                    description="Расширение ассортимента и сети пунктов выдачи.",
                ),
            ]
        )

    if not Partner.objects.filter(is_deleted=False).exists():
        Partner.objects.bulk_create(
            [
                Partner(
                    name="Royal Canin",
                    url="https://www.royalcanin.com/",
                    is_active=True,
                    sort_order=0,
                ),
                Partner(
                    name="Hills",
                    url="https://www.hillspet.com/",
                    is_active=True,
                    sort_order=1,
                ),
                Partner(
                    name="Purina",
                    url="https://www.purina.com/",
                    is_active=True,
                    sort_order=2,
                ),
            ]
        )

    if not Banner.objects.filter(is_deleted=False).exists():
        Banner.objects.bulk_create(
            [
                Banner(
                    title="Весенняя акция",
                    link_url="/shop/catalog/",
                    is_active=True,
                    sort_order=0,
                ),
                Banner(
                    title="Новинки для кошек",
                    link_url="/shop/catalog/",
                    is_active=True,
                    sort_order=1,
                ),
                Banner(
                    title="Скидки на корма",
                    link_url="/shop/catalog/",
                    is_active=True,
                    sort_order=2,
                ),
            ]
        )

    if not Contact.objects.filter(type="employee", is_deleted=False).exists():
        Contact.objects.bulk_create(
            [
                Contact(
                    type="employee",
                    value="ivanov-manager",
                    employee_name="Иван Иванов",
                    job_description="Менеджер зала: консультации по кормам и аксессуарам.",
                    phone_number="+375 (29) 111-11-11",
                    email_address="ivanov@zooshop.by",
                    is_primary=False,
                ),
                Contact(
                    type="employee",
                    value="petrova-support",
                    employee_name="Анна Петрова",
                    job_description="Оператор поддержки: ответы на вопросы клиентов.",
                    phone_number="+375 (29) 222-22-22",
                    email_address="petrova@zooshop.by",
                    is_primary=False,
                ),
                Contact(
                    type="employee",
                    value="sidorov-warehouse",
                    employee_name="Пётр Сидоров",
                    job_description="Кладовщик: комплектация заказов и самовывоз.",
                    phone_number="+375 (29) 333-33-33",
                    email_address="sidorov@zooshop.by",
                    is_primary=False,
                ),
            ]
        )

    for article in NewsArticle.objects.filter(is_deleted=False, summary=""):
        article.summary = f"Кратко: {article.title}."
        article.save(update_fields=["summary"])

    today = timezone.now().date()
    if not PromoCode.objects.filter(code="OLD2020").exists():
        PromoCode.objects.create(
            code="OLD2020",
            discount_percent=Decimal("10.00"),
            valid_from=today - timedelta(days=800),
            valid_until=today - timedelta(days=400),
            max_uses=50,
            current_uses=50,
            is_active=False,
        )
    if not PromoCode.objects.filter(code="EXPIRED").exists():
        PromoCode.objects.create(
            code="EXPIRED",
            discount_percent=Decimal("15.00"),
            valid_from=today - timedelta(days=90),
            valid_until=today - timedelta(days=1),
            max_uses=100,
            current_uses=10,
            is_active=True,
        )


def unseed_page_content(apps, schema_editor):
    # Keep data on reverse — demo content is safe to leave.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0004_lr_pages_extensions"),
        ("news", "0003_lr_pages_extensions"),
        ("promotions", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_page_content, unseed_page_content),
    ]
