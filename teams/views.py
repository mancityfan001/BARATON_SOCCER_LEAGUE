from urllib import request
from django.shortcuts import redirect
from django.shortcuts import render
from teams.models import Team
from players.models import Player
from matches.models import Match
from players.models import Transfer
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from .models import TeamPayment
from .models import RefereeProfile
from django.contrib.auth import authenticate, login
from finance.models import FinanceRecord
from datetime import date
from notifications.models import Notification, Announcement
from players.models import TransferPayment
from .models import Team
from notifications.models import AdminNotification
from players.models import Card
from django.contrib import messages

# HOME PAGE
def home(request):

    men_teams = Team.objects.filter(
        category='Men'
    ).order_by(
        '-points',
        '-goal_difference',
        '-goals_scored'
    )

    ladies_teams = Team.objects.filter(
        category='Ladies'
    ).order_by(
        '-points',
        '-goal_difference',
        '-goals_scored'
    )

    matches = Match.objects.all().order_by('-match_date')[:6]

    fixtures = Match.objects.filter(
        status='Pending'
    ).order_by('match_date')[:6]

    men_top_scorers = Player.objects.filter(
        team__category='Men',
        goals__gt=0
    ).order_by('-goals')[:5]

    ladies_top_scorers = Player.objects.filter(
        team__category='Ladies',
        goals__gt=0
    ).order_by('-goals')[:5]


    men_top_assists = Player.objects.filter(
        team__category='Men',
        assists__gt=0
    ).order_by('-assists')[:5]

    ladies_top_assists = Player.objects.filter(
        team__category='Ladies',
        assists__gt=0
    ).order_by('-assists')[:5]

    men_clean_sheets = Player.objects.filter(
        team__category='Men',
        position='Goalkeeper'
    ).order_by(
        '-clean_sheets',
        'goal_conceded'
    )[:5]

    ladies_clean_sheets = Player.objects.filter(
        team__category='Ladies',
        position='Goalkeeper'
    ).order_by(
        '-clean_sheets',
        'goal_conceded'
    )[:5]

    announcements = Announcement.objects.filter(
        audience='all'
    ).order_by('-created_at')

    context = {
        'men_teams': men_teams,
        'ladies_teams': ladies_teams,
        'matches': matches,
        'fixtures': fixtures,
        'men_top_scorers': men_top_scorers,
        'ladies_top_scorers': ladies_top_scorers,
        'men_top_assists': men_top_assists,
        'ladies_top_assists': ladies_top_assists,
        'men_clean_sheets': men_clean_sheets,
        'ladies_clean_sheets': ladies_clean_sheets,
        'announcements': announcements,
    }

    return render(request, 'core/home.html', context)


# COACH LOGIN
from django.contrib.auth import authenticate, login

def coach_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.role == "coach":

            login(request, user)

            return redirect('/dashboard/')
        
        else:

            return render(request, 'teams/coach_login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'teams/coach_login.html')

# COACH DASHBOARD
from players.models import Player
from notifications.models import Notification
from complaints.models import Complaint

def coach_dashboard(request):

    team = Team.objects.filter(coach=request.user).first()

    if team:
        players = Player.objects.filter(team=team)

        pending_transfers = Transfer.objects.filter(
            from_team=team,
            status='Pending'
        )

        approved_transfers = Transfer.objects.filter(
            to_team=team,
            status='Approved'  
        ).exclude(
            transferpayment__status='Approved'
        )
        print("APPROVED TRANSFERS:", approved_transfers)
    else:
        players = Player.objects.none()
        pending_transfers = Transfer.objects.none()
        approved_transfers = Transfer.objects.none()

    unread_count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()
    
    my_complaints = Complaint.objects.filter(
        coach=request.user
    ).order_by('-created_at')

    print("CURRENT USER:", request.user)
    print("MY COMPLAINTS:", my_complaints)

    context = {
        'players': players,
        'team': team,
        'pending_transfers': pending_transfers,
        'approved_transfers': approved_transfers,
        'unread_count': unread_count,
        'my_complaints': my_complaints
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

        position = request.POST.get('position')

        phone_number = request.POST.get('phone_number')

        team = Team.objects.filter(coach=request.user).first()

        Player.objects.create(
            player_name=player_name,
            age=age,
            jersey_number=jersey_number,
            school_id=school_id,
            position=position,
            phone_number=phone_number,
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
        transaction_code = request.POST.get('transaction_code')
        proof_of_payment = request.FILES.get('proof_of_payment')

        player = Player.objects.get(id=player_id)
        from_team = Team.objects.get(id=from_team_id)
        to_team = Team.objects.get(id=to_team_id)

        transfer = Transfer.objects.create(
            player=player,
            from_team=from_team,
            to_team=to_team,
            transaction_code=transaction_code,
            proof_of_payment=proof_of_payment,
            status='Pending'
        )

        AdminNotification.objects.create(
            title="Transfer Request",
            message=f"{from_team.name} requested transfer of {player.player_name} to {to_team.name}"
        )

        Notification.objects.create(
         user=from_team.coach,
         message=f"Transfer request received for {player.player_name} from {from_team.name} to {to_team.name}"
        )
        Notification.objects.create(
            user=request.user,
            message="Your transfer request has been submitted successfully."
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

    teams = Team.objects.all().order_by(
        'points',
        'goal_difference',
        'goals_scored'
    )

    if request.method == 'POST':

        team_id = request.POST.get('team')
        amount_paid = request.POST.get('amount_paid')
        mpesa_code = request.POST.get('mpesa_code')
        payment_proof = request.FILES.get('payment_proof')

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
            payment_proof=payment_proof
        )

        AdminNotification.objects.create(
            title="Team Registration Payment",
            message=f"{team.name} submitted a registration payment of KES{amount_paid}. {mpesa_code}"
        )
        FinanceRecord.objects.create(
            category='Team Registration',
            team=team,
            amount=amount_paid,
            description='Team registration payment',
            transaction_date=date.today(),
            transaction_code=mpesa_code,
            payment_proof=payment_proof,
            status='Pending',
            coach=request.user
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
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect

User = get_user_model()

def referee_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('full_name')
        license_number = request.POST.get('license_number')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.role = 'referee'
        user.is_active = False  # Set to False until admin approval
        user.phone_number = phone  # Set the phone number
        user.save()

        RefereeProfile.objects.create(
            user=user,
            full_name=full_name,
            license_number=license_number,
            phone_number=phone
        )

        AdminNotification.objects.create(
            title="New Referee Registration",
            message=f"{request.user.username} registered as a referee."
        )

        return redirect('/referee-login/')

    return render(request, 'teams/referee_login.html')
def referee_login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.role == "referee":

            login(request, user)

            return redirect('/referee-dashboard/')

    return render(
        request,
        'teams/referee_login_page.html'
    )

# REFEREE DASHBOARD
from matches.models import Match
from django.db import models

def referee_dashboard(request):

    referee = request.user

    assigned_matches = Match.objects.filter(
        models.Q(center_referee=request.user ) |
        models.Q(assistant_referee_one=request.user ) |
        models.Q(assistant_referee_two=request.user ) |
        models.Q(match_commissioner=request.user )
    ).order_by('match_date')

    announcements = Announcement.objects.filter(
        audience__in=['all', 'referees']
    ).order_by('-created_at')

    games_officiated = Match.objects.filter(
        center_referee=request.user ,
        status="Completed"
    ).count()

    context = {
        'assigned_matches': assigned_matches,
        'announcements': announcements,
        'games_officiated': games_officiated,
    }

    return render(
        request,
        'teams/referee_dashboard.html',
        context
    )

from django.shortcuts import redirect
from matches.models import MatchReport, CleanSheet

def submit_match_report(request):

    if request.method == "POST":

        match_id = request.GET.get("match")
        comments = request.POST.get("comments")
        incidents = request.POST.get("incidents")

        home_score = int(request.POST.get("home_score"))
        away_score = int(request.POST.get("away_score"))

        goal_scorer_ids = request.POST.getlist("goal_scorers")
        assist_player_ids = request.POST.getlist("assist_players")
        clean_sheet_keeper_ids = request.POST.getlist("clean_sheet_keepers")
        yellow_card_player_ids = request.POST.getlist("yellow_card_players")
        red_card_player_ids = request.POST.getlist("red_card_players")

        goal_scorer_names = []
        for player_id in goal_scorer_ids:
            if player_id:
                player = Player.objects.get(id=player_id)
                goal_scorer_names.append(player.player_name)

        assist_names = []
        for player_id in assist_player_ids:
            if player_id:
                player = Player.objects.get(id=player_id)
                assist_names.append(player.player_name)
        
        clean_sheet_names = []
        for player_id in clean_sheet_keeper_ids:
            if player_id:
                player = Player.objects.get(id=player_id)
                clean_sheet_names.append(player.player_name)

        yellow_card_names = []
        for player_id in yellow_card_player_ids:
            if player_id:
                player = Player.objects.get(id=player_id)
                yellow_card_names.append(player.player_name)

        red_card_names = []
        for player_id in red_card_player_ids:
            if player_id:
                player = Player.objects.get(id=player_id)
                red_card_names.append(player.player_name)

        match = Match.objects.get(id=match_id)

        if match.center_referee != request.user:
            messages.error(
                request,
                "Match report can only be submitted by the Center Referee."
            )
            return redirect('/referee-dashboard/')

        # Update match score
        match.home_score = home_score
        match.away_score = away_score
        match.status = "Completed"
        match.save()

        # ================= UPDATE LEAGUE TABLE =================

        # Prevent duplicate updates
        if MatchReport.objects.filter(match=match).exists():
            messages.error(request, "This match has already been reported.")
            return redirect("referee_dashboard")

        home_team = match.home_team
        away_team = match.away_team

        home_team.played += 1
        away_team.played += 1

        home_team.goals_scored += home_score
        home_team.goals_conceded += away_score

        away_team.goals_scored += away_score
        away_team.goals_conceded += home_score

        if home_score > away_score:
            home_team.wins += 1
            away_team.losses += 1
            home_team.points += 3

        elif home_score < away_score:
            away_team.wins += 1
            home_team.losses += 1
            away_team.points += 3

        else:
            home_team.draws += 1
            away_team.draws += 1
            home_team.points += 1
            away_team.points += 1

        home_team.goal_difference = (
            home_team.goals_scored -
            home_team.goals_conceded
        )

        away_team.goal_difference = (
            away_team.goals_scored -
            away_team.goals_conceded
        )

        home_team.save()
        away_team.save()

        # ================= END LEAGUE TABLE =================

        messages.success(
            request,
            "Match report submitted successfully."
        )

        # Save report
        MatchReport.objects.create(
            match=match,
            home_score=match.home_score,
            away_score=match.away_score,
            referee_comments=comments,
            incidents=incidents,
            goal_scorers=", ".join(goal_scorer_names),
            assist_providers=", ".join(assist_names),
            clean_sheet_keepers=", ".join(clean_sheet_names),
            yellow_card_players=", ".join(yellow_card_names),
            red_card_players=", ".join(red_card_names),
        )
        AdminNotification.objects.create(
            title="Match Report Submitted",
            message=f"Referee submitted a report for {match.home_team} vs {match.away_team}"
        )
            # Goal scorers
        for player_id in goal_scorer_ids:
            if not player_id:
                continue
            scorer = Player.objects.get(id=player_id)
            scorer.goals += 1
            scorer.save()

        # Assists
        for player_id in assist_player_ids:
            if not player_id:
                continue
            assister = Player.objects.get(id=player_id)
            assister.assists += 1
            assister.save()

        # Clean sheets
        for player_id in clean_sheet_keeper_ids:
            if not player_id:
                continue
            keeper = Player.objects.get(id=player_id)

            CleanSheet.objects.create(
                match=match,
                goalkeeper=keeper
            )

            keeper.clean_sheets += 1
            keeper.save()

        # Yellow cards
        for player_id in yellow_card_player_ids:
            if not player_id:
                continue
            player = Player.objects.get(id=player_id)

            Card.objects.create(
                player=player,
                match=match,
                card_type="Yellow",
                minute_given=0
            )

        # Red cards
        for player_id in red_card_player_ids:
            if not player_id:
                continue
            player = Player.objects.get(id=player_id)

            Card.objects.create(
                player=player,
                match=match,
                card_type="Red",
                minute_given=0
            )

        return redirect("referee_dashboard")

    

    matches = Match.objects.all()

    selected_match_id = request.GET.get('match')

    players = Player.objects.none()

    if selected_match_id:
        selected_match = Match.objects.get(id=selected_match_id)

        players = Player.objects.filter(
            team__in=[
                selected_match.home_team,
                selected_match.away_team
            ]
        )

    return render(
        request,
        "teams/submit_match_report.html",
        {
            "matches": matches,
            "players": players,
        }
    )

def approve_payment(request, payment_id):
    payment = get_object_or_404(TeamPayment, id=payment_id)
    payment.status = 'Approved'
    payment.save()
    Notification.objects.create(
        user=request.user,
        message=f"Your payment for {payment.team.team_name} has been approved."
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def reject_payment(request, payment_id):
    payment = get_object_or_404(TeamPayment, id=payment_id)
    payment.status = 'Rejected'
    payment.save()
    Notification.objects.create(
        user=request.user,
        message=f"Your payment for {payment.team.team_name} has been rejected."
    )
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()


def coach_register(request):

    if request.method == "POST":

        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        team_name = request.POST.get('team_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone_number')
        category = request.POST.get('category')

        if Team.objects.filter(name__iexact=team_name).exists():
            return render (
                request,
                'teams/coach_register.html',
                {
                    'error': 'A team with this name already exists.'
                  }
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.role = 'coach'
        user.phone_number = phone
        user.is_active = False  # Set to False until admin approval
        user.save()

        AdminNotification.objects.create(
            title="New Coach Registration",
            message=f"Coach {full_name} has registered their team {team_name}."
        )

        Team.objects.get_or_create(
            name=team_name,
            defaults={
                'coach': user,
                'phone_number': phone,
                'category': category
            }
        )

        return redirect('/login/')

    return render(
        request,
        'teams/coach_register.html'
    )
from players.models import Transfer

def transfer_requests(request):
    coach_team = Team.objects.get(coach=request.user)

    transfers = Transfer.objects.filter(
        from_team=coach_team,
        status='Pending'
    )

    return render(
        request,
        'teams/transfer_requests.html',
        {'transfers': transfers}
    )


def approve_transfer(request, transfer_id):

    transfer = Transfer.objects.get(id=transfer_id)

    transfer.status = 'Approved'
    transfer.save()
    Notification.objects.create(
        user=transfer.to_team.coach,
        message=f"Transfer approved for {transfer.player.player_name}"
    )

    return redirect('transfer_requests')


def reject_transfer(request, transfer_id):

    transfer = Transfer.objects.get(id=transfer_id)

    transfer.status = 'Rejected'
    transfer.save()
    Notification.objects.create(
        user=transfer.to_team.coach,
        message=f"Transfer rejected for {transfer.player.player_name}"
    )

    return redirect('transfer_requests')
def transfer_payment(request, transfer_id):

    transfer = Transfer.objects.get(id=transfer_id)

    if request.method == 'POST':

        amount = request.POST.get('amount')
        transaction_code = request.POST.get('transaction_code')
        proof_of_payment = request.FILES.get('proof_of_payment')

        payment = TransferPayment.objects.create(
            transfer=transfer,
            amount=amount,
            transaction_code=transaction_code,
            proof_of_payment=proof_of_payment
        )
        transfer.transaction_code =transaction_code
        transfer.proof_of_payment =proof_of_payment
        transfer.save()
        FinanceRecord.objects.create(
            category='Player Transfer',
            transfer=transfer,
            team=transfer.to_team,
            coach=transfer.to_team.coach,
            amount=amount,
            description=f"Transfer fee for {transfer.player.player_name}",
            transaction_date=date.today(),
            transaction_code=transaction_code,
            payment_proof=proof_of_payment,
            status='Pending'
    )
        return redirect('coach_dashboard')

    return render(
        request,
        'teams/transfer_payment.html',
        {'transfer': transfer}
    )
