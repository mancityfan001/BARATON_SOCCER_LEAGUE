from django.contrib import admin
from .models import TeamSheet
from django.utils.html import format_html

@admin.register(TeamSheet)
class TeamSheetAdmin(admin.ModelAdmin):

    list_display = (
        'team_name',
        'coach_name',
        'captain_name',
        'fixture',
        'approved',
        'print_teamsheet'
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

    def print_teamsheet(self, obj):
        return format_html(
            '<a href="/lineups/report/{}/" target="_blank">view / Print</a>',
            obj.id
        )
    print_teamsheet.short_description = "Print Team Sheet"