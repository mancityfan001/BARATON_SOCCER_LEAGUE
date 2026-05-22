from django.shortcuts import render, redirect
from django.contrib import messages

from players.models import Player
from .models import Injury


def report_injury(request):

    players = Player.objects.all()

    if request.method == 'POST':

        player_id = request.POST.get('player')

        injury_type = request.POST.get('injury_type')

        description = request.POST.get('description')

        injury_date = request.POST.get('injury_date')

        expected_return_date = request.POST.get(
            'expected_return_date'
        )

        player = Player.objects.get(id=player_id)

        Injury.objects.create(
            player=player,
            injury_type=injury_type,
            description=description,
            injury_date=injury_date,
            expected_return_date=expected_return_date,
        )

        messages.success(
            request,
            'Injury reported successfully.'
        )

        return redirect('report_injury')

    context = {
        'players': players
    }

    return render(
        request,
        'injuries/report_injury.html',
        context
    )