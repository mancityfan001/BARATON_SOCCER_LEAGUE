from django.contrib import admin
from .models import Notification, Announcement
from django.core.mail import send_mail
from django.conf import settings
from users.models import CustomUser
from .models import AdminNotification


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
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.audience == 'all':
            recipients = CustomUser.objects.exclude(email='')

        elif obj.audience == 'coaches':
            recipients = CustomUser.objects.filter(
                role='coach'
            ).exclude(email='')

        elif obj.audience == 'referees':
            recipients = CustomUser.objects.filter(
                role='referee'
            ).exclude(email='')

        else:
            recipients = CustomUser.objects.none() 
                
        for user in recipients:
                
            Notification.objects.create(
                user=user,
                message=f"{obj.title} : {obj.message}"
            )
            send_mail(
                obj.title,
                obj.message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True,
            )
@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_read', 'created_at')
    list_filter = ('is_read',)
    ordering = ('-created_at',)