from django.shortcuts import render
from teams.models import Team
from matches.models import Match
from players.models import Player


def home(request):

    teams = Team.objects.all().order_by('-points')

    matches = Match.objects.all()[:10]

    top_scorers = Player.objects.all().order_by('-goals')[:5]

    top_assists = Player.objects.all().order_by('-assists')[:5]

    clean_sheets = Player.objects.filter(
        position='Goalkeeper'
    ).order_by('-clean_sheets')[:5]

    context = {

        'teams': teams,

        'matches': matches,

        'top_scorers': top_scorers,

        'top_assists': top_assists,

        'clean_sheets': clean_sheets,

    }

    return render(request, 'core/home.html', context)