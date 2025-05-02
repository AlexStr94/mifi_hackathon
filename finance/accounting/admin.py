from django.contrib import admin

from audit.admin import UpdatedByAdminModel
from . import models


@admin.register(models.Bank)
class BankAdmin(UpdatedByAdminModel):
    pass


@admin.register(UpdatedByAdminModel)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UpdatedByAdminModel)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "transaction_type",
        "amount",
        "status",
        "sender_bank",
        "receiver_bank",
        "receiver_inn",
        "receiver_phone",
        "category",
    )
    list_filter = (
        "user",
        "transaction_type",
        "amount",
        "status",
        "sender_bank",
        "receiver_bank",
        "receiver_inn",
        "receiver_phone",
        "category",
    )
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "transaction_type",
        "amount",
        "status",
        "sender_bank__name",
        "receiver_bank__name",
        "receiver_inn",
        "receiver_phone",
        "category__name",
    )
