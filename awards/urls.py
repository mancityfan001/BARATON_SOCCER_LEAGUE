from django.urls import path
from . import views

urlpatterns = [
    path('', views.awards_page, name='awards'),
]