from django.contrib import admin
from django.urls import path, include
from teams import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Main Dashboard
    path('', views.home, name='home'),

    # Admin
    path('admin/register/', views.admin_register, name='admin_register'),
    path('admin/', admin.site.urls),

    # Coach Portal
    path('login/', views.coach_login, name='coach_login'),
    path( 'coach-register/', views.coach_register, name='coach_register'),
    path('dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('logout/', views.coach_logout, name='coach_logout'),

    path('register-player/', views.register_player, name='register_player'),
    path('request-transfer/', views.request_transfer, name='request_transfer'),
    path('teams/payment/', views.team_payment, name='team_payment'),

    #Referee Portal
    path('referee-login/', views.referee_login, name='referee_login'),
    path(
        'referee-login-page/',
        views.referee_login_page,
        name='referee_login_page'
    ),

    path(
        'referee-dashboard/',
        views.referee_dashboard,
        name='referee_dashboard'
    ),

    path(
        'submit-match-report/',
        views.submit_match_report,
        name='submit_match_report'
    ),
    
    # Other Apps
    path('notifications/', include('notifications.urls')),
    path('injuries/', include('injuries.urls')),
    path('finance/', include('finance.urls')),
    path('users/', include('users.urls')),
    path('matches/', include('matches.urls')),
    path('lineups/', include('lineups.urls')),
    path('complaints/', include('complaints.urls')),
    path('awards/', include('awards.urls')),
    path('reports/', include('reports.urls')),

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

    path(
    'transfer-requests/',
    views.transfer_requests,
    name='transfer_requests'
    ),

    path(
        'approve-transfer/<int:transfer_id>/',
        views.approve_transfer,
        name='approve_transfer'
    ),

    path(
        'reject-transfer/<int:transfer_id>/',
        views.reject_transfer,
        name='reject_transfer'
    ),

    path(
        'transfer-payment/<int:transfer_id>/',
        views.transfer_payment,
        name='transfer_payment'
    ),

    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )