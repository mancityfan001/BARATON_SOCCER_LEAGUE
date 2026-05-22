from urllib import request

from django.shortcuts import render, redirect
from teams.models import Team
from players.models import Player
from matches.models import Match
from players.models import Transfer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import TeamPayment


# HOME PAGE
def home(request):
    teams = Team.objects.all()
    matches = Match.objects.all()

    context = {
        'teams': teams,
        'matches': matches
    }

    return render(request, 'core/home.html', context)


# COACH LOGIN
def coach_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'coach' and password == '1234':
            return redirect('/dashboard/')

    return render(request, 'teams/coach_login.html')


# COACH DASHBOARD
from players.models import Player

def coach_dashboard(request):

    players = Player.objects.all()

    context = {
        'players': players
    }

    return render(
        request,
        'teams/coach_dashboard.html',
        context
    )


# LOGOUT
def coach_logout(request):
    return redirect('/')


# REGISTER PLAYER
from django.shortcuts import render, redirect
from players.models import Player
from teams.models import Team


def register_player(request):

    if request.method == 'POST':

        player_name = request.POST.get('player_name')

        age = request.POST.get('age')

        jersey_number = request.POST.get('jersey_number')

        school_id = request.POST.get('school_id')

        team = Team.objects.first()

        Player.objects.create(
            player_name=player_name,
            age=age,
            jersey_number=jersey_number,
            school_id=school_id,
            team=team
        )

        return redirect('/dashboard/')

    return render(
        request,
        'teams/register_player.html'
    )


# TRANSFER REQUEST
def request_transfer(request):

    players = Player.objects.all()
    teams = Team.objects.all()

    if request.method == 'POST':

        player_id = request.POST.get('player')
        from_team_id = request.POST.get('from_team')
        to_team_id = request.POST.get('to_team')
        transfer_fee = request.POST.get('transfer_fee')

        player = Player.objects.get(id=player_id)
        from_team = Team.objects.get(id=from_team_id)
        to_team = Team.objects.get(id=to_team_id)

        Transfer.objects.create(
            player=player,
            from_team=from_team,
            to_team=to_team,
            transfer_fee=transfer_fee,
            status='Pending'
        )

        return redirect('/dashboard/')

    context = {
        'players': players,
        'teams': teams
    }

    return render(request, 'teams/request_transfer.html', context)


# TEAM PAYMENT
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Team, TeamPayment
from notifications.models import Notification

def team_payment(request):

    teams = Team.objects.all()

    if request.method == 'POST':

        team_id = request.POST.get('team')
        amount_paid = request.POST.get('amount_paid')
        mpesa_code = request.POST.get('mpesa_code')

        # Check duplicate Mpesa code
        if TeamPayment.objects.filter(mpesa_code=mpesa_code).exists():

            messages.error(
                request,
                "This Mpesa code has already been used."
            )

            return redirect('team_payment')

        team = Team.objects.get(id=team_id)

        TeamPayment.objects.create(
            team=team,
            amount_paid=amount_paid,
            mpesa_code=mpesa_code,
        )
        Notification.objects.create(
             user=request.user,
             message="Your payment was submitted successfully and is awaiting admin approval."
)
    
        messages.success(
            request,
            "Payment submitted successfully. Await admin approval."
        )

        return redirect('team_payment')

    context = {
        'teams': teams
    }

    return render(
        request,
        'teams/payment.html',
        context
    )

# REFEREE LOGIN
def referee_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'referee' and password == '1234':
            return redirect('/referee-dashboard/')

    return render(request, 'teams/referee_login.html')

# REFEREE DASHBOARD
def referee_dashboard(request):

    matches = Match.objects.all()

    context = {
        'matches': matches,
        'games_count': matches.count()
    }

    return render(request, 'teams/referee_dashboard.html', context)
def approve_payment(request, payment_id):

    payment = get_object_or_404(
        TeamPayment,
        id=payment_id
    )

    payment.payment_status = 'Approved'
    payment.save()

    return HttpResponseRedirect(
        '/admin/teams/teampayment/'
    )


def reject_payment(request, payment_id):

    payment = get_object_or_404(
        TeamPayment,
        id=payment_id
    )

    payment.payment_status = 'Rejected'
    payment.save()

    return HttpResponseRedirect(
        '/admin/teams/teampayment/'
    )