from django.db import models
from players.models import Player
from teams.models import Team


class Award(models.Model):
    AWARD_TYPES = [
        ('Golden Boot', 'Golden Boot'),
        ('Golden Glove', 'Golden Glove'),
        ('Top Playmaker', 'Top Playmaker'),
        ('League Champion', 'League Champion'),
        ('Runner Up', 'Runner Up'),
        ('Fair Play', 'Fair Play'),
        ('Player of the Season', 'Player of the Season'),
        ('Team of the Season', 'Team of the Season'),
    ]

    season = models.CharField(max_length=20)

    award_name = models.CharField(
        max_length=50,
        choices=AWARD_TYPES
    )

    player = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    team = models.ForeignKey(
        Team,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    description = models.TextField(blank=True)

    date_awarded = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.award_name} ({self.season})"