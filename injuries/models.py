from django.db import models


class Injury(models.Model):

    STATUS_CHOICES = (
        ('Injured', 'Injured'),
        ('Recovering', 'Recovering'),
        ('Recovered', 'Recovered'),
    )

    player = models.ForeignKey(
        'players.Player',
        on_delete=models.CASCADE
    )

    injury_type = models.CharField(max_length=200)

    description = models.TextField()

    injury_date = models.DateField()

    expected_return_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Injured'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.player} - {self.injury_type}"