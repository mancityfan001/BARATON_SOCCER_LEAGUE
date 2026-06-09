from urllib import request

from django.shortcuts import render

import notifications
from .models import Notification

from django.db.models import Count

def notifications_page(request):
    notifications = Notification.objects.filter(
        user=request.user
).order_by('-created_at')

# Mark all as read when opened
    notifications.filter(
        is_read=False
).update(is_read=True)

    unread_count = 0

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    
    return render(
        request,
          'notifications/notifications.html',
            context
    )