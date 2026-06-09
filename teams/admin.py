from django.contrib import admin
from django.utils.html import format_html
from .models import RefereeProfile
from .models import Team, TeamPayment


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'coach',
        'phone_number',
        'category',
        'played',
        'wins',
        'draws',
        'losses',
        'goals_scored',
        'goals_conceded',
        'goal_difference',
        'points',
    )

    ordering = (
        '-points',
          '-goal_difference', 
          '-goals_scored'
          )


@admin.register(TeamPayment)
class TeamPaymentAdmin(admin.ModelAdmin):

    list_display = (
        'team',
        'amount_paid',
        'mpesa_code',
        'payment_status',
        'approve_button',
        'reject_button',
    )

    def approve_button(self, obj):

        if obj.payment_status == 'Pending':

            return format_html(
                '<a class="button" '
                'style="background-color:green; color:white; padding:5px 10px; text-decoration:none;" '
                'href="/admin/approve-payment/{}/">'
                'Approve</a>',
                obj.id
            )

        return "Approved"

    approve_button.short_description = 'Approve'


    def reject_button(self, obj):

        if obj.payment_status == 'Pending':

            return format_html(
                '<a class="button" '
                'style="background-color:red; color:white; padding:5px 10px; text-decoration:none;" '
                'href="/admin/reject-payment/{}/">'
                'Reject</a>',
                obj.id
            )

        return "Rejected"

    reject_button.short_description = 'Reject'
    admin.site.register(RefereeProfile)