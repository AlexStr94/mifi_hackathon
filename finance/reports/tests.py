from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounting.models import Transaction, Bank, Category


class ReportsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser', password='testpass'
        )
        bank = Bank.objects.create(name='Test Bank', inn='1234567890')
        category = Category.objects.create(name='Test Category', description='Test')

        # Создаём тестовые транзакции
        Transaction.objects.bulk_create([
            Transaction(
                user=cls.user,
                type_person='person',
                transaction_type='entry',
                amount=100,
                status='completed',
                sender_bank=bank,
                receiver_bank=bank,
                receiver_inn='1234567890',
                receiver_phone='+79990000000',
                category=category,
                date_time='2023-01-01'
            ),
            Transaction(
                user=cls.user,
                type_person='person',
                transaction_type='write-off',
                amount=50,
                status='completed',
                sender_bank=bank,
                receiver_bank=bank,
                receiver_inn='1234567890',
                receiver_phone='+79990000000',
                category=category,
                date_time='2023-01-02'
            )
        ])

    def test_report_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('reports:reports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Bank")
        self.assertContains(response, "Динамика транзакций")

    def test_report_data(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('reports:reports') + '?period=month')

        # Проверяем контекст
        self.assertTrue('transactions_dynamic' in response.context)
        self.assertTrue('income_expense' in response.context)

        # Проверяем данные
        self.assertEqual(response.context['income_expense']['income'], 100)
        self.assertEqual(response.context['income_expense']['expense'], 50)