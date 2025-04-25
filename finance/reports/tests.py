from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from accounting.models import Bank, Category, Transaction
from reports.views import generate_report_pdf
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class ReportsViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            inn="1234567890"
        )
        self.bank = Bank.objects.create(name="Test Bank", inn="1234567890")
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

        # Создаем тестовые транзакции
        Transaction.objects.create(
            user=self.user,
            type_person="company",
            date_time=timezone.now() - timedelta(days=1),
            transaction_type="entry",
            amount="1000.00",
            status="completed",
            sender_bank=self.bank,
            receiver_bank=self.bank,
            receiver_inn="1234567890",
            receiver_phone="+79998887766",
            category=self.category
        )
        Transaction.objects.create(
            user=self.user,
            type_person="person",
            date_time=timezone.now(),
            transaction_type="write-off",
            amount="500.00",
            status="completed",
            sender_bank=self.bank,
            receiver_bank=self.bank,
            receiver_inn="0987654321",
            receiver_phone="+79998887777",
            category=self.category
        )

    def test_generate_report_pdf(self):
        request = self.factory.get('/reports/')
        request.user = self.user

        # Тестируем генерацию PDF без параметров
        response = generate_report_pdf(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

        # Тестируем генерацию PDF с параметрами периода
        request = self.factory.get('/reports/?period=week')
        request.user = self.user
        response = generate_report_pdf(request)
        self.assertEqual(response.status_code, 200)


class ReportModelTest(TestCase):
    def test_report_generation(self):
        pass


class ReportTemplateTest(TestCase):
    def test_report_template_rendering(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            inn="1234567890"
        )
        self.client.force_login(self.user)

        response = self.client.get('/reports/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report.html')
        self.assertContains(response, "Финансовый отчет")