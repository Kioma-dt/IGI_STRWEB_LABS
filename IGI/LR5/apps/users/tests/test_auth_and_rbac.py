from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.test import Client, TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product, ProductStock
from apps.promotions.models import PromoCode
from apps.users.constants import GROUP_CUSTOMER, GROUP_EMPLOYEE
from apps.users.models import CustomerProfile

User = get_user_model()


def _phone(suffix: str) -> str:
    return f"+375 (29) {suffix[:3]}-{suffix[3:5]}-{suffix[5:7]}"


class AuthAndRBACTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.anon = APIClient()

    def test_register_jwt_and_rbac_endpoints(self) -> None:
        reg = self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "buyer@example.com",
                "password": "secretpass1",
                "password_confirm": "secretpass1",
                "full_name": "Buyer One",
                "phone": _phone("1234567"),
                "birth_date": str(date(1995, 5, 1)),
            },
            format="json",
        )
        self.assertEqual(reg.status_code, 201)
        user = User.objects.get(email="buyer@example.com")
        self.assertTrue(user.groups.filter(name=GROUP_CUSTOMER).exists())

        bad = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "buyer@example.com", "password": "wrong"},
            format="json",
        )
        self.assertEqual(bad.status_code, 401)

        tok = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "buyer@example.com", "password": "secretpass1"},
            format="json",
        )
        self.assertEqual(tok.status_code, 200)
        self.assertIsInstance(tok.data["access"], str)
        self.assertIsInstance(tok.data["refresh"], str)

        access = tok.data["access"]
        refresh = tok.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        mine = self.client.get("/api/v1/orders/mine/")
        self.assertEqual(mine.status_code, 200)

        emp = User.objects.create_user(
            username="worker@example.com",
            email="worker@example.com",
            password="workerpass12",
        )
        emp.groups.add(Group.objects.get(name=GROUP_EMPLOYEE))
        etok = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "worker@example.com", "password": "workerpass12"},
            format="json",
        )
        self.assertEqual(etok.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {etok.data['access']}")
        stats = self.client.get("/api/v1/orders/sales/stats/")
        self.assertEqual(stats.status_code, 200)
        self.assertIn("orders_total_count", stats.data)

        suppliers = self.client.get("/api/v1/suppliers/")
        self.assertEqual(suppliers.status_code, 200)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        denied = self.client.get("/api/v1/suppliers/")
        self.assertEqual(denied.status_code, 403)

    def test_jwt_refresh_and_blacklist_logout(self) -> None:
        self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "jwt@example.com",
                "password": "secretpass1",
                "password_confirm": "secretpass1",
                "full_name": "JWT User",
                "phone": _phone("7654321"),
                "birth_date": str(date(1990, 1, 1)),
            },
            format="json",
        )
        tok = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "jwt@example.com", "password": "secretpass1"},
            format="json",
        )
        refresh = tok.data["refresh"]
        new_tokens = self.client.post(
            "/api/v1/auth/jwt/refresh/",
            {"refresh": refresh},
            format="json",
        )
        self.assertEqual(new_tokens.status_code, 200)
        self.assertIn("access", new_tokens.data)
        new_refresh = new_tokens.data.get("refresh", refresh)
        out = self.client.post(
            "/api/v1/auth/jwt/logout/",
            {"refresh": new_refresh},
            format="json",
        )
        self.assertIn(out.status_code, (200, 205))

    def test_password_reset_confirm(self) -> None:
        u = User.objects.create_user(
            username="reset@example.com",
            email="reset@example.com",
            password="oldpassword12",
        )
        uid = urlsafe_base64_encode(force_bytes(u.pk))
        uid_str = uid.decode() if isinstance(uid, bytes) else uid
        token = default_token_generator.make_token(u)
        resp = self.client.post(
            "/api/v1/auth/password/reset/confirm/",
            {"uid": uid_str, "token": token, "new_password": "newpassword12"},
            format="json",
        )
        self.assertEqual(resp.status_code, 200)
        u.refresh_from_db()
        self.assertTrue(u.check_password("newpassword12"))

    def test_place_order_happy_path(self) -> None:
        self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "shopper@example.com",
                "password": "secretpass1",
                "password_confirm": "secretpass1",
                "full_name": "Shopper",
                "phone": _phone("3333333"),
                "birth_date": str(date(1992, 6, 6)),
            },
            format="json",
        )
        tok = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "shopper@example.com", "password": "secretpass1"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok.data['access']}")

        cat = Category.objects.create(name="C", slug="c-slug", parent=None)
        p = Product.objects.create(
            name="Item",
            sku="SKU-ORDER-1",
            category=cat,
            base_price=Decimal("5.00"),
        )
        ProductStock.objects.create(product=p, quantity_on_hand=10)

        po = self.client.post(
            "/api/v1/orders/place/",
            {"lines": [{"product_id": str(p.id), "quantity": 2}]},
            format="json",
        )
        self.assertEqual(po.status_code, 201, po.content)
        self.assertIn("reference_number", po.data)

    def test_session_login_respects_csrf_when_enforced(self) -> None:
        web = Client(enforce_csrf_checks=True)
        web.get("/api/v1/auth/csrf/")
        denied = web.post(
            "/api/v1/auth/session/login/",
            {"email": "csrf@example.com", "password": "x" * 12},
            content_type="application/json",
        )
        self.assertIn(denied.status_code, (400, 403, 419))

        User.objects.create_user(
            username="csrf@example.com",
            email="csrf@example.com",
            password="x" * 12,
        )
        csrftoken = web.cookies["csrftoken"].value
        ok = web.post(
            "/api/v1/auth/session/login/",
            {"email": "csrf@example.com", "password": "x" * 12},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=csrftoken,
        )
        self.assertEqual(ok.status_code, 200)

    def test_active_promotions_requires_permission(self) -> None:
        today = date.today()
        PromoCode.objects.create(
            code="SAVE10",
            discount_percent=Decimal("10.00"),
            valid_from=today - timedelta(days=1),
            valid_until=today + timedelta(days=30),
            is_active=True,
        )
        self.client.post(
            "/api/v1/auth/register/",
            {
                "email": "promo@example.com",
                "password": "secretpass1",
                "password_confirm": "secretpass1",
                "full_name": "Promo User",
                "phone": _phone("4444444"),
                "birth_date": str(date(1991, 1, 1)),
            },
            format="json",
        )
        tok = self.client.post(
            "/api/v1/auth/jwt/create/",
            {"username": "promo@example.com", "password": "secretpass1"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tok.data['access']}")
        r = self.client.get("/api/v1/promotions/active/")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.data), 1)
