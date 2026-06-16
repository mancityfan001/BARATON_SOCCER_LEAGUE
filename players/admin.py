from django.contrib import admin
from .models import Player, Card, Transfer
from notifications.models import Notification


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'player_name',
        'school_id',
        'age',
        'jersey_number',
        'phone_number',
        'position',
        'goals',
        'assists',
        'clean_sheets',
        'goal_conceded',
        'team',
        'is_suspended',
        'suspension_matches',
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'card_type',
        'match',
    )


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = (
        'player',
        'from_team',
        'to_team',
        'transaction_code',
        'status',
    )

    readonly_fields = (
        'proof_of_payment',
    )

    def save_model(self, request, obj, form, change):

        old_obj = None

        if obj.pk:
            old_obj = Transfer.objects.get(pk=obj.pk)

        super().save_model(request, obj, form, change)

        if (
            old_obj
            and old_obj.status != "Completed"
            and obj.status == "Completed"
        ):
            player = obj.player

            player.team = obj.to_team
            player.save()

            Notification.objects.create(
                user=obj.to_team.coach,
                message=f"Transfer approved for {player.player_name}"
            )

            Notification.objects.create(
                user=obj.to_team.coach,
                message=f"{player.player_name} has joined your team."
            )