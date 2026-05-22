from django.db import models


class Team(models.Model):

    name = models.CharField(max_length=100)

    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    goals_scored = models.IntegerField(default=0)
    goals_conceded = models.IntegerField(default=0)

    goal_difference = models.IntegerField(default=0)

    points = models.IntegerField(default=0)

    def __str__(self):
        
        return self.name

    # REGISTRATION PAYMENT

class TeamPayment(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    amount_paid = models.IntegerField()

    mpesa_code = models.CharField(
        max_length=20,
        unique=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.team} - {self.mpesa_code}"