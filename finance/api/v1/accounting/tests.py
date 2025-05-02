from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounting.models import Bank, Category, Transaction
from users.models import User


class TransactionFilterTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            inn='1234567890'
        )
        self.client.force_authenticate(user=self.user)

        self.bank = Bank.objects.create(name='Test Bank', inn='1234567890')
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )

        # Создаем несколько транзакций для тестирования фильтров
        Transaction.objects.create(
            user=self.user,
            type_person="company",
            date_time="2023-01-01T12:00:00Z",
            transaction_type="entry",
            comment="Test transaction 1",
            amount="1000.00000",
            status="completed",
            sender_bank=self.bank,
            receiver_bank=self.bank,
            receiver_inn="0987654321",
            receiver_phone="+79998887766",
            category=self.category
        )
        Transaction.objects.create(
            user=self.user,
            type_person="person",
            date_time="2023-01-02T12:00:00Z",
            transaction_type="write-off",
            comment="Test transaction 2",
            amount="500.00000",
            status="canceled",
            sender_bank=self.bank,
            receiver_bank=self.bank,
            receiver_inn="1234567890",
            receiver_phone="+79998887777",
            category=self.category
        )

    def test_filter_by_transaction_type(self):
        url = f"{reverse('transaction-list')}?transaction_type=entry"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['transaction_type'], 'Поступление')

    def test_filter_by_status(self):
        url = f"{reverse('transaction-list')}?status=canceled"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], 'Отменена')

    def test_filter_by_date_range(self):
        url = f"{reverse('transaction-list')}?date_after=2023-01-01&date_before=2023-01-01"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue('2023-01-01' in response.data[0]['date_time'])