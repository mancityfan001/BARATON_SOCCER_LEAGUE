from django.contrib import admin
from .models import Player, Card, Transfer


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = (
        'player_name',
        'school_id',
        'age',
        'jersey_number',
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
        'status',
    )