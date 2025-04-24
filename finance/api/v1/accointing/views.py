from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from accounting.models import Bank, Category, Transaction
from .filters import TransactionFilterSet
from .serializers import BankSerializer, CategorySerializer, CreateTransactionSerializer, RetrieveTransactionSerializer


class TransactionViewSet(ModelViewSet):
    """Реализация API методов для работы с транзакциями."""

    queryset = Transaction.objects.all()
    filterset_class = TransactionFilterSet
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Transaction.objects.all()
        return Transaction.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return CreateTransactionSerializer
        return RetrieveTransactionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BankViewSet(ReadOnlyModelViewSet):
    """Реализация API методов для работы с банками."""

    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = (IsAuthenticated,)


class CategoryViewSet(ReadOnlyModelViewSet):
    """Реализация API методов для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)
