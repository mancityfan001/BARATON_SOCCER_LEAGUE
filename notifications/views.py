from django.shortcuts import render
from .models import Notification

def notifications_page(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        'notifications': notifications
    }

    return render(
        request,
        'notifications/notifications.html',
        context
    )