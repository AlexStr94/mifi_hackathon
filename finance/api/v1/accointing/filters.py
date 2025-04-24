from django_filters import FilterSet

from accounting.models import Transaction


class TransactionFilterSet(FilterSet):
    """Класс для фильтрации транзакций."""

    class Meta:
        model = Transaction
        fields = (
            "sender_bank",
            "receiver_bank",
            "status",
            "receiver_inn",
            "category",
            "date_time",
        )
