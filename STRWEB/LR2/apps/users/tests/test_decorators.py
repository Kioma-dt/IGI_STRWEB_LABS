from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from apps.users.constants import GROUP_CUSTOMER
from apps.users.decorators import customer_required

User = get_user_model()


@customer_required
def _customer_only_view(request) -> HttpResponse:
    return HttpResponse("ok")


class CustomerRequiredDecoratorTests(TestCase):
    def test_anonymous_redirects(self) -> None:
        request = RequestFactory().get("/private/")
        request.user = AnonymousUser()
        response = _customer_only_view(request)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_non_customer_forbidden(self) -> None:
        user = User.objects.create_user(
            username="nocust@example.com",
            email="nocust@example.com",
            password="pw" * 8,
        )
        request = RequestFactory().get("/private/")
        request.user = user
        with self.assertRaises(PermissionDenied):
            _customer_only_view(request)

    def test_customer_allowed(self) -> None:
        user = User.objects.create_user(
            username="cust@example.com",
            email="cust@example.com",
            password="pw" * 8,
        )
        user.groups.add(Group.objects.get_or_create(name=GROUP_CUSTOMER)[0])
        request = RequestFactory().get("/private/")
        request.user = user
        response = _customer_only_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")
