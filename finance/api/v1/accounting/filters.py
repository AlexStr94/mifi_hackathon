from django_filters import FilterSet, NumberFilter

from accounting.models import Transaction


class TransactionFilterSet(FilterSet):
    """Класс для фильтрации транзакций."""

    amount_min = NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = NumberFilter(field_name='amount', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = (
            "sender_bank",
            "receiver_bank",
            "status",
            "receiver_inn",
            "category",
            "date_time",
            "amount_min",
            "amount_max"
        )
