from django.urls import path
from . import views

urlpatterns = [

    path(
        'add/',
        views.add_finance_record,
        name='add_finance_record'
    ),

]