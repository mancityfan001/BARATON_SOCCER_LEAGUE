from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta
from .models import CleanSheet
from .models import Match, MatchReport
from teams.models import Team


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    change_list_template = 'admin/matches/match/change_list.html'

    ordering= ('match_date',)
    
    list_display = (
        'category',
        'home_team',
        'away_team',
        'center_referee',
        'assistant_referee_one',
        'assistant_referee_two',
        'match_commissioner',
        'status',
        'match_date',
    )

    def category(self, obj):
        return obj.home_team.category
    
    category.short_description = "category"

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

        # Delete only pending fixtures
        Match.objects.filter(status="Pending").delete()

        start_date = timezone.now()

        def create_category_fixtures(category):
            nonlocal start_date

            teams = list(
                Team.objects.filter(category=category).order_by("id")
            )

            if len(teams) < 2:
                return []

            # Add BYE if odd number of teams
            if len(teams) % 2 == 1:
                teams.append(None)

            n = len(teams)
            rounds = n - 1
            half = n // 2

            rotation = teams[:]

            first_leg = []

            # ---------------- FIRST LEG ----------------
            for r in range(rounds):

                weekly_matches = []

                for i in range(half):

                    home = rotation[i]
                    away = rotation[n - 1 - i]

                    if home is None or away is None:
                        continue

                    # Alternate home advantage
                    if r % 2 == 1:
                        home, away = away, home

                    weekly_matches.append((home, away))

                first_leg.append(weekly_matches)

                # Rotate teams
                rotation = (
                    [rotation[0]]
                    + [rotation[-1]]
                    + rotation[1:-1]
                )
    
            # Save first leg
            first_leg_matches = []

            for week in first_leg:
                for home, away in week:
                    first_leg_matches.append({
                        "home": home,
                        "away": away,
                        "leg": 1,
                    })

            # ---------------- SECOND LEG ----------------
            second_leg_matches = []

            for week in first_leg:
                for home, away in week:
                    second_leg_matches.append({
                        "home": away,
                        "away": home,
                        "leg": 2,
                    })

            return first_leg_matches + second_leg_matches   

        # Generate each league separately
        men_matches = create_category_fixtures("Men")
        ladies_matches = create_category_fixtures("Ladies")

        all_matches = []

        men_matches = men_matches or []
        ladies_matches = ladies_matches or []

        men_count = len(men_matches)
        ladies_count = len(ladies_matches)

        if men_count == 0:
            all_matches = ladies_matches

        elif ladies_count == 0:
            all_matches = men_matches

        else:
            interval = max(1, round(men_count / ladies_count))

            m = 0
            l = 0

            while m < men_count or l < ladies_count:

                for _ in range(interval):
                    if m < men_count:
                        all_matches.append(men_matches[m])
                        m += 1

                if l < ladies_count:
                    all_matches.append(ladies_matches[l])
                    l += 1

            while m < men_count:
                all_matches.append(men_matches[m])
                m += 1

            while l < ladies_count:
                all_matches.append(ladies_matches[l])
                l += 1

        for fixture in all_matches:

            Match.objects.create(
                home_team=fixture["home"],
                away_team=fixture["away"],
                home_score=0,
                away_score=0,
                status="Pending",
                match_date=start_date,
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
        'home_score',
        'away_score',
        'created_at',
    )

@admin.register(CleanSheet)
class CleanSheetAdmin(admin.ModelAdmin):
    list_display = (
        'match',
        'goalkeeper',
    )