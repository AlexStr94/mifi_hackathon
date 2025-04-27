from rest_framework import serializers

from accounting.models import Bank, Category, Transaction


class BankSerializer(serializers.ModelSerializer):
    """Сериализация банков."""

    class Meta:
        model = Bank
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Сериализация категорий"""

    class Meta:
        model = Category
        fields = "__all__"


class CreateTransactionSerializer(serializers.ModelSerializer):
    """Сериализация транзакций при создании."""

    class Meta:
        model = Transaction
        fields = (
            "type_person",
            "date_time",
            "transaction_type",
            "comment",
            "amount",
            "status",
            "sender_bank",
            "receiver_bank",
            "receiver_inn",
            "receiver_phone",
            "category",
        )


class RetrieveTransactionSerializer(serializers.ModelSerializer):
    """Сериализация транзакций при отображении."""

    user = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    receiver_bank = serializers.StringRelatedField()
    sender_bank = serializers.StringRelatedField()
    transaction_type = serializers.CharField(source='get_transaction_type_display')
    type_person = serializers.CharField(source='get_type_person_display')

    class Meta:
        model = Transaction
        fields = (
            "user",
            "type_person",
            "date_time",
            "transaction_type",
            "comment",
            "amount",
            "status",
            "sender_bank",
            "receiver_bank",
            "receiver_inn",
            "receiver_phone",
            "category",
        )
