from django.contrib import admin

from .models import AuditLog


class UpdatedByAdminModel(admin.ModelAdmin):
    exclude = ("updated_by",)

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "entity", "obj_id", "timestamp",)
