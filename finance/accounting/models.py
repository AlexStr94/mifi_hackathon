from django.db import models

from audit.models import UpdatedByModel


class Bank(UpdatedByModel):
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


class Category(UpdatedByModel):
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


class Transaction(UpdatedByModel):
    PERSON_TYPES = (
        ("company", "Юридическое лицо"),
        ("person", "Физическое лицо"),
    )
    TRANSACTION_TYPES = (
        ("entry", "Поступление"),
        ("write-off", "Списание"),
    )
    TRANSACTION_STATUSES = (
        ('new', 'Новая'),
        ('confirmed', 'Подтвержденная'),
        ('in_process', 'В обработке'),
        ('canceled', 'Отменена'),
        ('completed', 'Платеж выполнен'),
        ('deleted', 'Платеж удален'),
        ('refund', 'Возврат')
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

    def __str__(self):
        return f"Транзакция {self.id}"
