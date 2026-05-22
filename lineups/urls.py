from django.urls import path
from . import views

urlpatterns = [

    path(
        'submit/',
        views.submit_teamsheet,
        name='submit_teamsheet'
    ),

   
]