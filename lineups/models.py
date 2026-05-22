from django.db import models
from matches.models import Match


class TeamSheet(models.Model):

    fixture = models.ForeignKey(
        Match,
        on_delete=models.CASCADE
    )

    team_name = models.CharField(max_length=100)

    coach_name = models.CharField(max_length=100)

    captain_name = models.CharField(max_length=100)

    first_eleven = models.TextField()

    substitutes = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.team_name} Team Sheet"