from django.contrib import admin
from .models import Complaint
from notifications.models import Notification


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'subject',
        'coach',
        'status',
        'created_at'
    )

    def save_model(self, request, obj, form, change):

        if change:
            old_obj = Complaint.objects.get(pk=obj.pk)

            if (
                not old_obj.admin_response
                and obj.admin_response
            ):
                Notification.objects.create(
                    user=obj.coach,
                    message=f"Admin responded to your complaint: {obj.subject}\n\nResponse: {obj.admin_response}"
            )

        super().save_model(
            request,
            obj,
            form,
            change
        )