from django.db import models


class Match(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Played', 'Played'),

    )

    home_team = models.ForeignKey(

        'teams.Team',

        on_delete=models.CASCADE,

        related_name='home_matches'

    )

    away_team = models.ForeignKey(

        'teams.Team',

        on_delete=models.CASCADE,

        related_name='away_matches'

    )

    home_score = models.IntegerField(

        default=0

    )

    away_score = models.IntegerField(

        default=0

    )

    venue = models.CharField(

        max_length=100

    )

    match_date = models.DateTimeField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='Pending'

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"{self.home_team} vs {self.away_team}"


class MatchReport(models.Model):

    match = models.OneToOneField(

        Match,

        on_delete=models.CASCADE

    )

    referee_comments = models.TextField()

    incidents = models.TextField()

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"Report - {self.match}"