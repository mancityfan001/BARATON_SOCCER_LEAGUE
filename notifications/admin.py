from django.contrib import admin
from .models import Notification, Announcement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    
    list_display = (
        'user',
        'message',
        'is_read',
        'created_at',
    )

    @admin.register(Announcement)
    class AnnouncementAdmin(admin.ModelAdmin):
        list_display = (
            'title',
            'created_at',
        )