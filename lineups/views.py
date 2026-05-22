from django.shortcuts import render, redirect
from .models import TeamSheet
from matches.models import Match


def submit_teamsheet(request):

    matches = Match.objects.all()

    if request.method == 'POST':

        fixture_id = request.POST.get('fixture')

        fixture = Match.objects.get(id=fixture_id)

        team_name = request.POST.get('team_name')

        coach_name = request.POST.get('coach_name')

        captain_name = request.POST.get('captain_name')

        first_eleven = request.POST.get('first_eleven')

        substitutes = request.POST.get('substitutes')

        TeamSheet.objects.create(
            fixture=fixture,
            team_name=team_name,
            coach_name=coach_name,
            captain_name=captain_name,
            first_eleven=first_eleven,
            substitutes=substitutes
        )

        return redirect('/dashboard/')

    return render(
        request,
        'lineups/submit_teamsheet.html',
        {'matches': matches}
    )