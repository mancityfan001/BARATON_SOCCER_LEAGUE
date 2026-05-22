from django.core.management.base import BaseCommand
from matches.models import Match
from teams.models import Team
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Generate double round robin fixtures'

    def handle(self, *args, **kwargs):

        Match.objects.all().delete()

        teams = list(Team.objects.all())

        start_date = timezone.now()

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

        self.stdout.write(
            self.style.SUCCESS('Fixtures generated successfully')
        )