from django.urls import path
from . import views

urlpatterns = [

    path(
        'referee-login/',
        views.referee_login,
        name='referee_login'
    ),

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
]