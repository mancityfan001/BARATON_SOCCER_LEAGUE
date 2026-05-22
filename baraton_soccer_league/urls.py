from django.contrib import admin
from django.urls import path, include
from teams import views

urlpatterns = [

    # Main Dashboard
    path('', views.home, name='home'),

    # Admin
    path('admin/', admin.site.urls),

    # Coach Portal
    path('login/', views.coach_login, name='coach_login'),
    path('dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('logout/', views.coach_logout, name='coach_logout'),

    path('register-player/', views.register_player, name='register_player'),
    path('request-transfer/', views.request_transfer, name='request_transfer'),
    path('teams/payment/', views.team_payment, name='team_payment'),

    # Other Apps
    path('notifications/', include('notifications.urls')),
    path('injuries/', include('injuries.urls')),
    path('finance/', include('finance.urls')),
    path('users/', include('users.urls')),
    path('matches/', include('matches.urls')),
    path('lineups/', include('lineups.urls')),

    # Payment Approval
    path(
        'approve-payment/<int:payment_id>/',
        views.approve_payment,
        name='approve_payment'
    ),

    path(
        'reject-payment/<int:payment_id>/',
        views.reject_payment,
        name='reject_payment'
    ),

    # Referee Portal
    path('referee-login/', views.referee_login, name='referee_login'),
    path('referee-dashboard/', views.referee_dashboard, name='referee_dashboard'),

]