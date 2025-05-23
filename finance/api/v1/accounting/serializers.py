from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class UpdateTransactionSerializer(serializers.ModelSerializer):
    """Сериализация транзакций при создании."""

    class Meta:
        model = Transaction
        fields = (
            "type_person",
            "date_time",
            "comment",
            "amount",
            "status",
            "sender_bank",
            "receiver_bank",
            "receiver_inn",
            "receiver_phone",
            "category",
        )

    def update(self, instance, validated_data):
        if instance.status in Transaction.NOT_UPDATABLE_STATUSES:
            raise ValidationError(f"Нельзя редактировать транзакцию со статусом {instance.get_status_display()}")
        return super().update(instance, validated_data)


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
            "id",
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
            "updatable",
        )
