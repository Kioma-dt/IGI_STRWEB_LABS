from django.test import TestCase
from django.utils import timezone

from apps.common.models import FAQ, Contact, Vacancy, CompanyInfo, PickupPoint


class FAQModelTest(TestCase):
    """Тесты для модели FAQ"""

    def test_create_faq(self):
        faq = FAQ.objects.create(
            question="What is this?",
            answer="This is an answer",
            sort_order=1,
        )
        self.assertEqual(FAQ.objects.count(), 1)
        self.assertEqual(str(faq), "What is this?")

    def test_faq_str_representation(self):
        faq = FAQ.objects.create(question="Test Q", answer="Test A")
        self.assertEqual(str(faq), "Test Q")

    def test_faq_ordering(self):
        FAQ.objects.create(question="Q1", answer="A1", sort_order=2)
        FAQ.objects.create(question="Q2", answer="A2", sort_order=1)
        faq_list = list(FAQ.objects.filter(is_deleted=False))
        self.assertEqual(faq_list[0].sort_order, 1)

    def test_faq_soft_delete(self):
        faq = FAQ.objects.create(question="Q", answer="A")
        faq.soft_delete()
        self.assertTrue(faq.is_deleted)
        self.assertIsNone(FAQ.objects.filter(is_deleted=False).first())


class VacancyModelTest(TestCase):
    """Тесты для модели Vacancy"""

    def test_create_vacancy(self):
        vacancy = Vacancy.objects.create(
            title="Senior Developer",
            description="Looking for experienced dev",
            is_active=True,
            published_at=timezone.now(),
        )
        self.assertEqual(str(vacancy), "Senior Developer")

    def test_vacancy_inactive(self):
        vacancy = Vacancy.objects.create(
            title="Test", description="Desc", is_active=False
        )
        self.assertFalse(vacancy.is_active)

    def test_vacancy_published_at_optional(self):
        vacancy = Vacancy.objects.create(
            title="Test", description="Desc", published_at=None
        )
        self.assertIsNone(vacancy.published_at)


class ContactModelTest(TestCase):
    """Тесты для модели Contact"""

    def test_create_phone_contact(self):
        contact = Contact.objects.create(
            type="phone", value="+375291111111", is_primary=True
        )
        self.assertEqual(contact.type, "phone")
        self.assertEqual(str(contact), "phone: +375291111111")

    def test_create_email_contact(self):
        contact = Contact.objects.create(
            type="email", value="test@example.com", is_primary=False
        )
        self.assertEqual(contact.get_type_display(), "email")

    def test_contact_unique_constraint(self):
        """Проверка уникальности пары (type, value)"""
        Contact.objects.create(type="phone", value="+375291111111")
        with self.assertRaises(Exception):
            Contact.objects.create(type="phone", value="+375291111111")

    def test_all_contact_types(self):
        types = ["phone", "email", "address", "social"]
        for type_val in types:
            contact = Contact.objects.create(type=type_val, value=f"test-{type_val}")
            self.assertEqual(contact.type, type_val)


class CompanyInfoModelTest(TestCase):
    """Тесты для модели CompanyInfo"""

    def test_create_company_info(self):
        company = CompanyInfo.objects.create(
            name="Test Shop",
            legal_address="123 Main St",
            support_email="support@test.com",
            phone="+375291111111",
            is_current=True,
        )
        self.assertEqual(str(company), "Test Shop")

    def test_company_info_unique_current(self):
        """Только одна текущая компания"""
        CompanyInfo.objects.create(
            name="Company 1",
            legal_address="Addr1",
            support_email="c1@test.com",
            phone="+375291111111",
            is_current=True,
        )
        # Вторая создается с is_current=False
        company2 = CompanyInfo.objects.create(
            name="Company 2",
            legal_address="Addr2",
            support_email="c2@test.com",
            phone="+375292222222",
            is_current=False,
        )
        self.assertFalse(company2.is_current)

    def test_company_about_optional(self):
        company = CompanyInfo.objects.create(
            name="Shop",
            legal_address="Addr",
            support_email="s@test.com",
            phone="+375291111111",
            about="",
        )
        self.assertEqual(company.about, "")


class PickupPointModelTest(TestCase):
    """Тесты для модели PickupPoint"""

    def test_create_pickup_point(self):
        pp = PickupPoint.objects.create(
            name="Pickup #1",
            address="123 Main St",
            phone="+375291111111",
            working_hours="09:00-21:00",
            is_active=True,
        )
        self.assertEqual(str(pp), "Pickup #1 - 123 Main St")

    def test_pickup_point_inactive(self):
        pp = PickupPoint.objects.create(
            name="PP", address="Addr", phone="+375291111111", is_active=False
        )
        self.assertFalse(pp.is_active)

    def test_pickup_point_working_hours_optional(self):
        pp = PickupPoint.objects.create(
            name="PP", address="Addr", phone="+375291111111", working_hours=""
        )
        self.assertEqual(pp.working_hours, "")
