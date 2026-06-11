from django.shortcuts import render
from notifications.models import Announcement, Notification
from teams.models import Team
from matches.models import Match
from players.models import Player


def home(request):

    print("HOME VIEW RUNNING")

    # LEAGUE TABLE
    teams = Team.objects.all().order_by(
        '-points',
        '-goal_difference',
        '-goals_scored'
    )

    # RECENT MATCHES
    matches = Match.objects.filter(
        status='Played'
    ).order_by('-match_date')[:6]

    # UPCOMING FIXTURES
    fixtures = Match.objects.filter(
        status='Pending'
    ).order_by('match_date')[:6]

    # TOP SCORERS
    top_scorers = Player.objects.all().order_by(
        '-goals'
    )[:5]

    # TOP ASSISTS
    top_assists = Player.objects.all().order_by(
        '-assists'
    )[:5]

    # CLEAN SHEETS
    clean_sheets = Player.objects.filter(
        position='Goalkeeper'
    ).order_by(
        '-clean_sheets',
        'goal_conceded'
    )[:5]

    # NOTIFICATIONS
    announcements = Announcement.objects.filter(
        audience='all'
    ).order_by('-created_at')
    
    context = {

        'teams': teams,

        'matches': matches,

        'fixtures': fixtures,

        'top_scorers': top_scorers,

        'top_assists': top_assists,

        'clean_sheets': clean_sheets,
        
        'announcements': announcements,
    }

    return render(
        request,
        'core/home.html',
        context
    )