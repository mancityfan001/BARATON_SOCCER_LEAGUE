from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

from .models import Match, MatchReport
from teams.models import Team


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    change_list_template = 'admin/matches/match/change_list.html'

    ordering= ('match_date',)
    
    list_display = (
        'home_team',
        'away_team',
        'center_referee',
        'assistant_referee_one',
        'assistant_referee_two',
        'match_commissioner',
        'status',
        'match_date',
    )

    actions = ['generate_fixtures']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'generate-fixtures/',
                self.admin_site.admin_view(
                    self.generate_fixtures_view
                    ),
                name='generate-fixtures',
            ),
        ]
        return custom_urls + urls
    
    def generate_fixtures(self, request, queryset):

        # DELETE OLD FIXTURES
        pending_matches = Match.objects.filter(status='Pending')
        pending_matches.delete()

        teams = list(Team.objects.all())

        if len(teams) < 2:
            self.message_user(
                request,
                "Add at least 2 teams first."
            )
            return

        start_date = timezone.now()

        # DOUBLE ROUND ROBIN
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):

                home_team = teams[i]
                away_team = teams[j]

                # FIRST LEG
                Match.objects.create(
                    home_team=home_team,
                    away_team=away_team,
                    home_score=0,
                    away_score=0,
                    status='Pending',
                    match_date=start_date
                )

                start_date += timedelta(days=7)

                # SECOND LEG
                Match.objects.create(
                    home_team=away_team,
                    away_team=home_team,
                    home_score=0,
                    away_score=0,
                    status='Pending',
                    match_date=start_date
                )

                start_date += timedelta(days=7)

        self.message_user(
            request,
            "Fixtures generated successfully."
        )

    generate_fixtures.short_description = (
        "Generate Double Round Robin Fixtures"
    )

    def generate_fixtures_view(self, request):
        self.generate_fixtures(
            request, 
            Match.objects.none()
        )
        return redirect('..')


@admin.register(MatchReport)
class MatchReportAdmin(admin.ModelAdmin):

    list_display = (
        'match',
        'created_at',
    )