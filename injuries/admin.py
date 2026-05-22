from django.contrib import admin
from .models import Injury


@admin.register(Injury)
class InjuryAdmin(admin.ModelAdmin):

    list_display = (
        'player',
        'injury_type',
        'injury_date',
        'expected_return_date',
        'status',
    )