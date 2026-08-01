from django.shortcuts import render, redirect
from .models import TeamSheet
from matches.models import Match
from django.shortcuts import get_object_or_404


def submit_teamsheet(request):

    matches = Match.objects.filter(
        status='Pending'
        ).order_by('match_date')

    if request.method == 'POST':

        fixture_id = request.POST.get('fixture')

        fixture = Match.objects.get(id=fixture_id)

        team_name = request.POST.get('team_name')

        coach_name = request.POST.get('coach_name')

        captain_name = request.POST.get('captain_name')

        first_eleven = "\n".join([
            request.POST.get('goalkeeper', ''),
            request.POST.get('left_back', ''),
            request.POST.get('center_back_1', ''),
            request.POST.get('center_back_2', ''),
            request.POST.get('right_back', ''),
            request.POST.get('midfielder_1', ''),
            request.POST.get('midfielder_2', ''),
            request.POST.get('midfielder_3', ''),
            request.POST.get('left_wing', ''),
            request.POST.get('striker', ''),
            request.POST.get('right_wing', '')
        ])

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

def teamsheet_report(request, teamsheet_id):
    teamsheet = get_object_or_404(TeamSheet, id=teamsheet_id)

    first_eleven = teamsheet.first_eleven.splitlines()

    substitutes = (
    teamsheet.substitutes.splitlines() 
    if teamsheet.substitutes
    else []
    )
    context = {
        'teamsheet': teamsheet,
        'first_eleven': first_eleven,
        'substitutes': substitutes
    }
    return render(request, 'lineups/teamsheet_report.html', context)