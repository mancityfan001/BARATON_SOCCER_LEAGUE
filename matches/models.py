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
    
    def save(self, *args, **kwargs):
        # Save the match first
        super().save(*args, **kwargs)

        # Recalculate team statistics from all played matches
        # Note: status value for completed matches is 'Played'
        matches = Match.objects.filter(status='Played')

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

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"Report - {self.match}"