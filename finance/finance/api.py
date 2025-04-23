from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounting.models import Transaction
from finance.serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)