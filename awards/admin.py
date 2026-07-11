from django.contrib import admin
from .models import Award


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = (
        'award_name',
        'season',
        'player',
        'team',
        'date_awarded'
    )

    list_filter = (
        'season',
        'award_name'
    )

    search_fields = (
        'award_name',
        'season'
    )