from django.db import models
from django.conf import settings


class Match(models.Model):

    STATUS_CHOICES = (

        ('Pending', 'Pending'),

        ('Live', 'Live'),

        ('Completed', 'Completed'),

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

    center_referee = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='center_referee_matches'
)

    assistant_referee_one = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assistant_referee_one_matches'
)

    assistant_referee_two = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assistant_referee_two_matches'
)

    match_commissioner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='commissioner_matches'
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

    def save(self, *args, **kwargs):
        # Save the match first
        super().save(*args, **kwargs)

        # Recalculate team statistics from all played matches
        # Note: status value for completed matches is 'Completed'
        matches = Match.objects.filter(status='Completed')

        # Reset all related teams' stats used below before recomputing
        teams = set()
        for m in matches:
            teams.add(m.home_team_id)
            teams.add(m.away_team_id)

        from teams.models import Team

        for team_id in teams:
            team = Team.objects.get(pk=team_id)
            team.played = 0
            team.wins = 0
            team.draws = 0
            team.losses = 0
            team.goals_scored = 0
            team.goals_conceded = 0
            team.goal_difference = 0
            team.points = 0
            team.save()

        for match in matches:
            home = match.home_team
            away = match.away_team

            home.played += 1
            away.played += 1

            home.goals_scored += match.home_score
            home.goals_conceded += match.away_score

            away.goals_scored += match.away_score
            away.goals_conceded += match.home_score

            if match.home_score > match.away_score:
                home.wins += 1
                home.points += 3
                away.losses += 1
            elif match.home_score < match.away_score:
                away.wins += 1
                away.points += 3
                home.losses += 1
            else:
                home.draws += 1
                away.draws += 1
                home.points += 1
                away.points += 1

            home.goal_difference = home.goals_scored - home.goals_conceded
            away.goal_difference = away.goals_scored - away.goals_conceded

            home.save()
            away.save()

class MatchReport(models.Model):

    match = models.OneToOneField(

        Match,

        on_delete=models.CASCADE

    )

    referee_comments = models.TextField()

    incidents = models.TextField()

    goal_scorers = models.TextField(blank=True)
    assist_providers = models.TextField(blank=True)
    clean_sheet_keepers = models.TextField(blank=True)
    yellow_card_players = models.TextField(blank=True)
    red_card_players = models.TextField(blank=True)

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"Report - {self.match}"
    
from players.models import Player


class Goal(models.Model):
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='goals'
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    minute = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.player_name}"
    

class CleanSheet(models.Model):

    match = models.ForeignKey(
         Match,
         on_delete=models.CASCADE
    )

    goalkeeper = models.ForeignKey(
         Player,
         on_delete=models.CASCADE
    )

    def __str__(self):
         return self.goalkeeper.player_name