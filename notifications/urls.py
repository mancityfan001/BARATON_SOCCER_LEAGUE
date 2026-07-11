from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.notifications_page,
        name='notifications'
    ),

    path(
        'clear-all-notifications/',
        views.clear_all_notifications,
        name='clear_all_notifications'
    ),
]