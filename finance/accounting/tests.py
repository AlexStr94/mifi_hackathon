from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Bank, Category, Transaction
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class BankModelTest(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(
            name="Test Bank",
            inn="1234567890"
        )

    def test_bank_creation(self):
        self.assertEqual(self.bank.name, "Test Bank")
        self.assertEqual(self.bank.inn, "1234567890")
        self.assertEqual(str(self.bank), "Test Bank")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "Test Description")
        self.assertEqual(str(self.category), "Test Category")


class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            inn="1234567890"
        )
        self.bank = Bank.objects.create(
            name="Test Bank",
            inn="0987654321"
        )
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description"
        )
        self.transaction = Transaction.objects.create(
            user=self.user,
            type_person="company",
            date_time=timezone.now(),
            transaction_type="entry",
            amount="1000.00",
            status="completed",
            sender_bank=self.bank,
            receiver_bank=self.bank,
            receiver_inn="1234567890",
            receiver_phone="+79998887766",
            category=self.category
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.type_person, "company")
        self.assertEqual(self.transaction.transaction_type, "entry")
        self.assertEqual(self.transaction.amount, 1000.00)
        self.assertEqual(self.transaction.status, "completed")
        self.assertEqual(str(self.transaction), f"Transaction #{self.transaction.id}")

    def test_transaction_get_type_person_display(self):
        self.assertEqual(
            self.transaction.get_type_person_display(),
            "Юридическое лицо"
        )

    def test_transaction_get_transaction_type_display(self):
        self.assertEqual(
            self.transaction.get_transaction_type_display(),
            "Поступление"
        )


class TransactionQuerySetTest(TestCase):
    def setUp(self):
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

    def test_transaction_queryset(self):
        transactions = Transaction.objects.filter(user=self.user)
        self.assertEqual(transactions.count(), 2)

        entries = transactions.filter(transaction_type="entry")
        self.assertEqual(entries.count(), 1)
        self.assertEqual(entries.first().amount, 1000.00)

        write_offs = transactions.filter(transaction_type="write-off")
        self.assertEqual(write_offs.count(), 1)
        self.assertEqual(write_offs.first().amount, 500.00)