from django.urls import path
from . import views

urlpatterns = [

    path(
        'submit/',
        views.submit_teamsheet,
        name='submit_teamsheet'
    ),

    path(
        'report/<int:teamsheet_id>/',
        views.teamsheet_report,
        name='teamsheet_report'
    )

]