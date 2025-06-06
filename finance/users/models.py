from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    inn = models.CharField(
        "ИНН",
        max_length=12,
        unique=True,
        null=True,
    )
    created_at = models.DateTimeField(
        "Пользователь зарегистрирован",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Последнее обновление пользователя",
        auto_now=True,
    )
