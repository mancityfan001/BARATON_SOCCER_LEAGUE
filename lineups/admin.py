from django.contrib import admin
from .models import TeamSheet


@admin.register(TeamSheet)
class TeamSheetAdmin(admin.ModelAdmin):

    list_display = (
        'team_name',
        'coach_name',
        'captain_name',
        'fixture',
        'approved'
    )

    list_filter = (
        'approved',
    )

    search_fields = (
        'team_name',
        'coach_name',
        'captain_name',
    )

    actions = ['approve_teamsheets']

    def approve_teamsheets(self, request, queryset):
        queryset.update(approved=True)

    approve_teamsheets.short_description = "Approve selected team sheets"