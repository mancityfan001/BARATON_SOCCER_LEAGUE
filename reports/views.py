from django.shortcuts import render

from teams.models import Team
from players.models import Player
from matches.models import Match
from finance.models import FinanceRecord
from awards.models import Award


def reports(request):

    men_teams = Team.objects.filter(category='Men').order_by(
        '-points',
        '-goal_difference'
    )

    ladies_teams = Team.objects.filter(category='Ladies').order_by(
        '-points',
        '-goal_difference'
    )

    top_scorers = Player.objects.order_by('-goals')[:10]

    top_assists = Player.objects.order_by('-assists')[:10]

    clean_sheets = Player.objects.filter(
        position='Goalkeeper'
    ).order_by('-clean_sheets')[:10]

    matches = Match.objects.order_by('-match_date')

    finance = FinanceRecord.objects.order_by('-transaction_date')

    awards = Award.objects.order_by('-season')

    context = {
        'men_teams': men_teams,
        'ladies_teams': ladies_teams,
        'top_scorers': top_scorers,
        'top_assists': top_assists,
        'clean_sheets': clean_sheets,
        'matches': matches,
        'finance': finance,
        'awards': awards,
    }

    return render(request, 'reports/report.html', context)