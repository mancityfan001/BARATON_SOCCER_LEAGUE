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

]