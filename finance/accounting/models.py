from django.db import models


class Bank(models.Model):
    name = models.CharField(
        "Наименования банка",
        max_length=256,
        unique=True,
    )
    inn = models.CharField(
        "ИНН",
        max_length=10,
        unique=True,
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        "Название категории.",
        max_length=128,
        unique=True,
    )
    description = models.CharField(
        "Описание категории.",
        max_length=256,
    )
    created_at = models.DateTimeField(
        "Дата и время создания категории.",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Дата и время последнего обновления категории.",
        auto_now=True,
    )

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    NEW_TRANSACTION = "new"
    CONFIRMED_TRANSACTION = "confirmed"
    IN_PROCESS_TRANSACTION = "in_process"
    CANCELED_TRANSACTION = "canceled"
    COMPLETED_TRANSACTION = "completed"
    DELETED_TRANSACTION = "deleted"
    REFUND_TRANSACTION = "refund"
    NOT_UPDATABLE_STATUSES = (
        CONFIRMED_TRANSACTION,
        IN_PROCESS_TRANSACTION,
        CANCELED_TRANSACTION,
        COMPLETED_TRANSACTION,
        DELETED_TRANSACTION,
        REFUND_TRANSACTION
    )
    TRANSACTION_STATUSES = (
        (NEW_TRANSACTION, 'Новая'),
        (CONFIRMED_TRANSACTION, 'Подтвержденная'),
        (IN_PROCESS_TRANSACTION, 'В обработке'),
        (CANCELED_TRANSACTION, 'Отменена'),
        (COMPLETED_TRANSACTION, 'Платеж выполнен'),
        (DELETED_TRANSACTION, 'Платеж удален'),
        (REFUND_TRANSACTION, 'Возврат')
    )
    PERSON_TYPES = (
        ("company", "Юридическое лицо"),
        ("person", "Физическое лицо"),
    )
    TRANSACTION_TYPES = (
        ("entry", "Поступление"),
        ("write-off", "Списание"),
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Идентификатор пользователя, который создал транзакцию."
    )
    type_person = models.CharField(
        verbose_name="Тип лица",
        choices=PERSON_TYPES,
        max_length=10,
    )
    date_time = models.DateTimeField(
        "Дата и время операции.",
    )
    transaction_type = models.CharField(
        "Тип транзакции",
        choices=TRANSACTION_TYPES,
        max_length=10,
    )
    comment = models.CharField(
        "Комментарий к операции.",
        max_length=500,
        blank=True
    )
    amount = models.DecimalField(
        "Сумма транзакции.",
        decimal_places=5,
        max_digits=20,
    )
    status = models.CharField(
        "Статус операции",
        choices=TRANSACTION_STATUSES,
        max_length=10,
    )
    sender_bank = models.ForeignKey(
        to=Bank,
        on_delete=models.PROTECT,
        related_name="sent_transactions",
    )
    receiver_bank = models.ForeignKey(
        to=Bank,
        on_delete=models.PROTECT,
        related_name="received_transactions",
    )
    receiver_inn = models.CharField(
        "ИНН",
        max_length=12,
    )
    receiver_phone = models.CharField(
        "Телефон получателя",
        max_length=18,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    @property
    def updatable(self) -> bool:
        if self.status in self.NOT_UPDATABLE_STATUSES:
            return False
        return True
