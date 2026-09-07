from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from apps.users.models import CustomerProfile, EmployeeProfile, ShopPermission


class CustomerProfileModelTest(TestCase):
    """Тесты для модели CustomerProfile"""

    def setUp(self):
        self.user = User.objects.create_user("customer", "c@test.com", "pass123")

    def test_create_customer_profile(self):
        profile = CustomerProfile.objects.create(
            user=self.user,
            first_name="John",
            middle_name="",
            last_name="Doe",
            phone="+375291111111",
            birth_date=date(1990, 1, 15),
        )
        self.assertEqual(profile.first_name, "John")
        self.assertEqual(profile.last_name, "Doe")

    def test_customer_profile_vip_status(self):
        profile = CustomerProfile.objects.create(user=self.user, is_vip=True)
        self.assertTrue(profile.is_vip)

    def test_customer_profile_non_vip(self):
        profile = CustomerProfile.objects.create(user=self.user, is_vip=False)
        self.assertFalse(profile.is_vip)

    def test_customer_profile_soft_delete(self):
        profile = CustomerProfile.objects.create(user=self.user)
        profile.soft_delete()
        self.assertTrue(profile.is_deleted)

    def test_customer_optional_fields(self):
        profile = CustomerProfile.objects.create(
            user=self.user,
            first_name="",
            middle_name="",
            last_name="",
            phone="",
            birth_date=None,
        )
        self.assertEqual(profile.first_name, "")
        self.assertIsNone(profile.birth_date)


class EmployeeProfileModelTest(TestCase):
    """Тесты для модели EmployeeProfile"""

    def setUp(self):
        self.user = User.objects.create_user("employee", "e@test.com", "pass123")

    def test_create_employee_profile(self):
        profile = EmployeeProfile.objects.create(
            user=self.user, phone="+375291111111", position="Manager"
        )
        self.assertEqual(profile.position, "Manager")
        self.assertEqual(profile.phone, "+375291111111")

    def test_employee_profile_position_optional(self):
        profile = EmployeeProfile.objects.create(user=self.user, phone="+375291111111")
        self.assertEqual(profile.position, "")

    def test_employee_profile_soft_delete(self):
        profile = EmployeeProfile.objects.create(user=self.user, phone="+375291111111")
        profile.soft_delete()
        self.assertTrue(profile.is_deleted)


class ShopPermissionModelTest(TestCase):
    """Тесты для модели ShopPermission"""

    def test_shop_permission_creation(self):
        perm = ShopPermission.objects.create(
            codename="place_order", name="Can place orders"
        )
        self.assertEqual(perm.codename, "place_order")
        self.assertEqual(perm.name, "Can place orders")

    def test_all_permission_types(self):
        permissions = [
            "place_order",
            "view_own_orders",
            "manage_products",
            "manage_suppliers",
            "manage_staff",
        ]
        for codename in permissions:
            perm = ShopPermission.objects.create(
                codename=codename, name=f"Permission: {codename}"
            )
            self.assertEqual(perm.codename, codename)

    def test_unique_codename(self):
        ShopPermission.objects.create(codename="unique_perm", name="Test")
        with self.assertRaises(Exception):
            ShopPermission.objects.create(codename="unique_perm", name="Test2")
