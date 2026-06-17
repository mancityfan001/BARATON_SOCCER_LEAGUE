from .models import AdminNotification

def admin_notifications(request):
    return {
        'unread_notifications':
        AdminNotification.objects.filter(
            is_read=False
        ).count()
    }