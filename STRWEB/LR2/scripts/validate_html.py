#!/usr/bin/env python
"""Validate rendered store pages with the W3C Nu Html Checker."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zooshop.settings.dev")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import django

django.setup()

from django.test import Client
from django.urls import reverse

from apps.catalog.models import Product
from apps.common.models import Vacancy
from apps.news.models import NewsArticle
from apps.orders.models import Order
from apps.suppliers.models import Supplier
from apps.users.models import EmployeeProfile


VALIDATOR_URL = "https://validator.w3.org/nu/?out=json"


@dataclass(frozen=True)
class Page:
    name: str
    path_factory: Callable[[], str]
    authenticated: bool = False


def first_or_none(queryset):
    return queryset.filter(is_deleted=False).first()


def build_pages() -> list[Page]:
    product = first_or_none(Product.objects.filter(is_active=True))
    article = first_or_none(NewsArticle.objects.filter(is_published=True))
    vacancy = first_or_none(Vacancy.objects.filter(is_active=True))
    supplier = first_or_none(Supplier.objects.filter(is_active=True))
    order = first_or_none(Order.objects.all())

    pages = [
        Page("home", lambda: reverse("store:home")),
        Page("about", lambda: reverse("store:about")),
        Page("news_list", lambda: reverse("store:news-list")),
        Page("faq", lambda: reverse("store:faq")),
        Page("contacts", lambda: reverse("store:contacts")),
        Page("privacy", lambda: reverse("store:privacy")),
        Page("vacancy_list", lambda: reverse("store:vacancy-list")),
        Page("catalog", lambda: reverse("store:catalog")),
        Page("cart", lambda: reverse("store:cart")),
        Page("checkout", lambda: reverse("store:checkout")),
        Page("payment", lambda: reverse("store:payment")),
        Page("reviews", lambda: reverse("store:reviews")),
        Page("promos", lambda: reverse("store:promos")),
        Page("pickup_points", lambda: reverse("store:pickup-points")),
        Page("login", lambda: reverse("store:login")),
        Page("signup", lambda: reverse("store:signup")),
        Page("employee_signup", lambda: reverse("store:employee-signup")),
        Page("account", lambda: reverse("store:account"), authenticated=True),
        Page(
            "account_orders",
            lambda: reverse("store:account-orders"),
            authenticated=True,
        ),
        Page("suppliers", lambda: reverse("store:supplier-list"), authenticated=True),
        Page("orders", lambda: reverse("store:order-list"), authenticated=True),
    ]

    if product:
        pages.append(
            Page(
                "product_detail",
                lambda product=product: reverse(
                    "store:product-detail",
                    kwargs={"pk": product.pk},
                ),
            )
        )
    if article:
        pages.append(
            Page(
                "news_detail",
                lambda article=article: reverse(
                    "store:news-detail",
                    kwargs={"pk": article.pk},
                ),
            )
        )
    if vacancy:
        pages.append(
            Page(
                "vacancy_apply",
                lambda vacancy=vacancy: reverse(
                    "store:vacancy-apply",
                    kwargs={"pk": vacancy.pk},
                ),
            )
        )
    if supplier:
        pages.append(
            Page(
                "supplier_detail",
                lambda supplier=supplier: reverse(
                    "store:supplier-detail",
                    kwargs={"pk": supplier.pk},
                ),
                authenticated=True,
            )
        )
    if order:
        pages.append(
            Page(
                "order_detail",
                lambda order=order: reverse(
                    "store:order-detail",
                    kwargs={"pk": order.pk},
                ),
                authenticated=True,
            )
        )

    return pages


def validate_page(client: Client, page: Page) -> dict:
    path = page.path_factory()
    response = client.get(path, follow=True)
    if response.status_code >= 400:
        raise RuntimeError(f"GET {path} returned HTTP {response.status_code}")

    request = urllib.request.Request(
        VALIDATOR_URL,
        data=response.content,
        headers={
            "Content-Type": "text/html; charset=utf-8",
            "User-Agent": "LR1HtmlValidator/1.0",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=90) as validator_response:
        data = json.load(validator_response)

    messages = data.get("messages", [])
    errors = [message for message in messages if message.get("type") == "error"]
    return {
        "path": path,
        "status_code": response.status_code,
        "errors": len(errors),
        "warnings": len([message for message in messages if message.get("type") != "error"]),
        "samples": [
            {
                "line": message.get("lastLine"),
                "column": message.get("lastColumn"),
                "message": message.get("message"),
            }
            for message in errors[:6]
        ],
    }


def main() -> int:
    anonymous_client = Client()
    employee_client = Client()
    employee_profile = EmployeeProfile.objects.filter(is_deleted=False).first()

    if employee_profile:
        employee_client.force_login(employee_profile.user)

    results = {}
    for page in build_pages():
        client = employee_client if page.authenticated and employee_profile else anonymous_client
        try:
            results[page.name] = validate_page(client, page)
        except (urllib.error.URLError, ValueError, RuntimeError) as exc:
            results[page.name] = {
                "path": page.path_factory(),
                "errors": -1,
                "error": str(exc),
            }

    has_errors = False
    for name, result in results.items():
        errors = result.get("errors", -1)
        warnings = result.get("warnings", 0)
        status = "OK" if errors == 0 else "ERROR"
        print(f"{status}: {name} ({result['path']}) - errors: {errors}, warnings: {warnings}")
        if result.get("error"):
            print(f"  check failed: {result['error']}")
        for sample in result.get("samples", []):
            print(f"  line {sample['line']}: {sample['message']}")
        if errors != 0:
            has_errors = True

    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
