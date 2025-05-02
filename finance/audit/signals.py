from datetime import datetime
from decimal import Decimal
import json
from typing import Any
from django.db.models import Model
from django.db.models.signals import pre_save, post_delete

from accounting.models import Bank, Category, Transaction
from .models import AuditLog


def serialize_model_field(field_value: Any) -> Any:
    if issubclass(field_value.__class__, Model):
        return field_value.id
    if isinstance(field_value, datetime):
        return field_value.isoformat()
    if isinstance(field_value, Decimal):
        return str(field_value)
    return None


def log_create_update(sender, instance, **kwargs):
    previous = sender.objects.get(id=instance.id)
    changes = {}
    if instance.id is None:
        action = AuditLog.CREATE_ACTION
    else:
        action = AuditLog.UPDATE_ACTION
        for field in sender._meta.fields:
            previous_value = getattr(previous, field.name)
            new_value = getattr(instance, field.name)
            if previous_value != new_value:
                changes[field.name] = {
                    "previous": previous_value,
                    "new_value": new_value,
                }

    AuditLog.objects.create(
        user=instance.updated_by,
        action=action,
        entity=sender.__name__,
        obj_id=instance.pk,
        changes=json.dumps(obj=changes, default=serialize_model_field),
    )


def log_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance.updated_by,
        action=AuditLog.DELETE_ACTION,
        entity=sender.__name__,
        obj_id=instance.pk,
        changes={}
    )


pre_save.connect(log_create_update, sender=Transaction)
post_delete.connect(log_delete, Transaction)
pre_save.connect(log_create_update, sender=Bank)
post_delete.connect(log_delete, Bank)
pre_save.connect(log_create_update, sender=Category)
post_delete.connect(log_delete, Category)
