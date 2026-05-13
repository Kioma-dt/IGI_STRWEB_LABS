from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from apps.catalog.models import Category, Product
from apps.users.constants import GROUP_CUSTOMER, GROUP_EMPLOYEE
from apps.users.models import CustomerProfile


def _phone(suffix: str) -> str:
    return f"+375 (29) {suffix[:3]}-{suffix[3:5]}-{suffix[5:7]}"


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
        "DEFAULT_FILTER_BACKENDS": [
            "django_filters.rest_framework.DjangoFilterBackend",
            "rest_framework.filters.SearchFilter",
            "rest_framework.filters.OrderingFilter",
        ],
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework_simplejwt.authentication.JWTAuthentication",
        ],
        "DEFAULT_PAGINATION_CLASS": "presentation.api.pagination.ZoomShopPageNumberPagination",
        "PAGE_SIZE": 20,
        "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",
        "DEFAULT_VERSION": "1",
        "ALLOWED_VERSIONS": ("1",),
        "VERSION_PARAM": "version",
        "DEFAULT_THROTTLE_CLASSES": [],
        "DEFAULT_THROTTLE_RATES": {},
        "EXCEPTION_HANDLER": "presentation.api.exceptions.zoomshop_exception_handler",
    },
)
class ZoomShopRestAPITests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.cat = Category.objects.create(name="Dogs", slug="dogs", parent=None)
        self.product = Product.objects.create(
            name="Kibble",
            sku="KIB-1",
            category=self.cat,
            base_price=Decimal("12.00"),
        )
        self.staff = self._create_user(
            "staff@example.com",
            is_staff=True,
            groups=(),
        )
        self.employee = self._create_user(
            "emp@example.com",
            is_staff=False,
            groups=("employee",),
        )
        self.customer_user = self._create_user(
            "cust@example.com",
            is_staff=False,
            groups=("customer",),
        )
        CustomerProfile.objects.create(
            user=self.customer_user,
            full_name="Cust One",
            birth_date=date(1990, 1, 1),
            phone=_phone("9999999"),
        )

    def _create_user(
        self,
        email: str,
        *,
        is_staff: bool,
        groups: tuple[str, ...],
    ):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        u = User.objects.create_user(
            username=email,
            email=email,
            password="password12345",
            is_staff=is_staff,
        )
        for g in groups:
            u.groups.add(Group.objects.get(name=g))
        return u

    def _jwt(self, user) -> str:
        url = "/api/v1/auth/jwt/create/"
        r = self.client.post(
            url,
            {"username": user.email, "password": "password12345"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK, r.content)
        return r.data["access"]

    def test_products_list_anonymous(self) -> None:
        r = self.client.get("/api/products/", {"version": "1"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(r.data.get("count", 0), 1)

    def test_products_search(self) -> None:
        r = self.client.get("/api/products/", {"search": "Kibble", "version": "1"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(r.data.get("count", 0), 1)

    def test_categories_ordering(self) -> None:
        r = self.client.get("/api/categories/", {"ordering": "name", "version": "1"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_invalid_api_version(self) -> None:
        r = self.client.get("/api/products/", {"version": "99"})
        # QueryParameterVersioning raises NotFound for unknown versions (DRF default).
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_list_requires_sales_permission(self) -> None:
        token = self._jwt(self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.get("/api/orders/", {"version": "1"})
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list_employee_jwt(self) -> None:
        token = self._jwt(self.employee)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.get("/api/orders/", {"version": "1"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_product_create_requires_permission(self) -> None:
        token = self._jwt(self.customer_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.post(
            "/api/products/",
            {
                "name": "X",
                "sku": "SKU-X-NEW",
                "category": str(self.cat.id),
                "description": "",
                "base_price": "1.00",
                "age_restriction": 0,
                "is_active": True,
                "initial_stock": 0,
            },
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_create_staff(self) -> None:
        token = self._jwt(self.staff)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.post(
            "/api/products/",
            {
                "name": "Staff product",
                "sku": "SKU-STAFF-1",
                "category": str(self.cat.id),
                "description": "",
                "base_price": "3.00",
                "age_restriction": 0,
                "is_active": True,
                "initial_stock": 5,
            },
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED, r.content)
        self.assertEqual(r.data.get("name"), "Staff product")

    def test_reviews_list_anonymous(self) -> None:
        self.client.credentials()
        r = self.client.get("/api/reviews/", {"version": "1"})
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_exception_envelope_on_404(self) -> None:
        import uuid

        r = self.client.get(f"/api/products/{uuid.uuid4()}/", {"version": "1"})
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", r.data)
        self.assertIn("status", r.data)
