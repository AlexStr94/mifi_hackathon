from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand

from accounting.models import Bank, Category, Transaction
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self._create_user()
        self._create_banks()
        self._create_category()
        self._create_transactions()

    def _create_user(self):
        self.user, _ = User.objects.get_or_create(
            username="test",
            email="test@gmail.com",
            first_name="Иван",
            last_name="Иванов",
            is_staff=False,
            is_active=True,
        )
        self.user.set_password("superhardpassword1")
        self.user.save()
    
    def _create_banks(self):
        self.bank, _ = Bank.objects.get_or_create(
            name="П-банк",
            inn="1234567890"
        )

    def _create_category(self):
        self.category, _ = Category.objects.get_or_create(
            name="Еда"
        )

    def _create_transactions(self):
        transactions = []
        for _ in range(1000): 
            start_date = datetime(2024, 1, 1)
            end_date = datetime.now()

            # Генерируем случайное количество дней между стартовой и конечной датами
            delta_days = (end_date - start_date).days
            random_days = random.randint(0, delta_days)

            # Получаем рандомную дату
            random_date = start_date + timedelta(days=random_days)

            code = random.randint(900, 999)  # Например, мобильный код
            part1 = random.randint(100, 999)
            part2 = random.randint(10, 99)
            part3 = random.randint(10, 99)
            phone =  f"+7 ({code}) {part1}-{part2}-{part3}"
            transactions.append(
                Transaction(
                    user=self.user,
                    type_person="person",
                    date_time=random_date,
                    transaction_type=random.choice(Transaction.TRANSACTION_TYPES)[0],
                    comment="Вкусно.",
                    amount=random.randint(1, 10000),
                    status=random.choice(Transaction.TRANSACTION_STATUSES)[0],
                    sender_bank=self.bank,
                    receiver_bank=self.bank,
                    receiver_phone=phone,
                    category=self.category,
                )
            )

        Transaction.objects.bulk_create(transactions, batch_size=200)

        