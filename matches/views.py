from django.shortcuts import render

from django.http import HttpResponse

from .models import Match

from matches.models import Match

from django.shortcuts import redirect

from django.contrib import messages

from django.utils import timezone

from teams.models import Team

from datetime import datetime, timedelta


def fixtures(request):

    fixtures = Match.objects.filter(

        status='Pending'

    ).order_by('match_date')

    context = {

        'fixtures': fixtures

    }

    return render(

        request,

        'matches/fixtures.html',

        context

    )


def results(request):

    results = Match.objects.filter(

        status='Played'

    ).order_by('-match_date')

    context = {

        'results': results

    }

    return render(

        request,

        'matches/results.html',

        context

    )


def generate_fixtures(request):

    Match.objects.all().delete()

    start_date = timezone.now()

    def create_category_fixtures(category):
        nonlocal start_date

        teams = list(Team.objects.filter(category=category))

        if len(teams) < 2:
            return

        # Add BYE if odd number of teams
        if len(teams) % 2 == 1:
            teams.append(None)

        n = len(teams)
        rounds = n - 1
        half = n // 2

        rotation = teams[:]
        first_leg = []

        # FIRST LEG
        for round_number in range(rounds):

            weekly_matches = []

            for i in range(half):
                home = rotation[i]
                away = rotation[n - 1 - i]

                if home is not None and away is not None:

                    if round_number % 2 == 0:
                        weekly_matches.append((home, away))
                    else:
                        weekly_matches.append((away, home))

            first_leg.append(weekly_matches)

            # Rotate teams
            rotation = (
                [rotation[0]]
                + [rotation[-1]]
                + rotation[1:-1]
            )

        # Save first leg
        for week in first_leg:
            for home, away in week:
                Match.objects.create(
                    home_team=home,
                    away_team=away,
                    home_score=0,
                    away_score=0,
                    status="Pending",
                    match_date=start_date,
                )

            start_date += timedelta(days=7)

        # Save second leg
        for week in first_leg:
            for home, away in week:
                Match.objects.create(
                    home_team=away,
                    away_team=home,
                    home_score=0,
                    away_score=0,
                    status="Pending",
                    match_date=start_date,
                )

            start_date += timedelta(days=7)

    # Generate fixtures separately
    create_category_fixtures("Men")
    create_category_fixtures("Ladies")

    return HttpResponse("Fixtures generated successfully.")