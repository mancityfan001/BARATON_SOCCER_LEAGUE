from django.contrib import admin

from .models import Match, MatchReport


@admin.register(Match)

class MatchAdmin(admin.ModelAdmin):

    list_display = (

        'home_team',

        'away_team',

        'home_score',

        'away_score',

        'status',

        'match_date'

    )


@admin.register(MatchReport)

class MatchReportAdmin(admin.ModelAdmin):

    list_display = (

        'match',

        'created_at'

    )