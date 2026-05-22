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

    teams = list(Team.objects.all())

    if len(teams) < 2:

        return HttpResponse(
            "Add at least 2 teams first."
        )

    Match.objects.all().delete()

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

    return HttpResponse(
        "Fixtures generated successfully."
    )