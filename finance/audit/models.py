from django.db import models

from users.models import User


class UpdatedByModel(models.Model):
    updated_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    """Лог действий пользователя, изменяющих состояние БД."""

    CREATE_ACTION = "create"
    UPDATE_ACTION = "update"
    DELETE_ACTION = "delete"

    ACTIONS = (
        (CREATE_ACTION, "Создание"),
        (UPDATE_ACTION, "Обновление"),
        (DELETE_ACTION, "Удаление"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField("Действие", max_length=10, choices=ACTIONS)
    entity = models.CharField("Сущность", max_length=100)
    obj_id = models.CharField("ID объекта", max_length=100)
    timestamp = models.DateTimeField("Время", auto_now_add=True)
    changes = models.JSONField()
