from django.shortcuts import render

from django.http import HttpResponse

from .models import Match

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

    start_date = datetime.now()

    days_gap = 7

    fixture_count = 0

    for i in range(len(teams)):

        for j in range(i + 1, len(teams)):

            home_team = teams[i]

            away_team = teams[j]

            match_date = (

                start_date +

                timedelta(

                    days=fixture_count * days_gap

                )

            )

            Match.objects.create(

                home_team=home_team,

                away_team=away_team,

                match_date=match_date,

                venue='Baraton Stadium',

                status='Pending'

            )

            fixture_count += 1

    return HttpResponse(

        "Fixtures generated successfully."

    )