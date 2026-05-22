from django.shortcuts import render, redirect
from django.contrib import messages

from teams.models import Team
from .models import FinanceRecord


def add_finance_record(request):

    teams = Team.objects.all()

    if request.method == 'POST':

        category = request.POST.get('category')

        team_id = request.POST.get('team')

        amount = request.POST.get('amount')

        description = request.POST.get('description')

        transaction_date = request.POST.get(
            'transaction_date'
        )

        team = None

        if team_id:

            team = Team.objects.get(id=team_id)

        FinanceRecord.objects.create(

            category=category,

            team=team,

            amount=amount,

            description=description,

            transaction_date=transaction_date,

        )

        messages.success(
            request,
            'Finance record added successfully.'
        )

        return redirect('add_finance_record')

    context = {
        'teams': teams
    }

    return render(
        request,
        'finance/add_finance_record.html',
        context
    )