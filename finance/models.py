from django.db import models


class FinanceRecord(models.Model):

    CATEGORY_CHOICES = (

        ('Team Registration', 'Team Registration'),

        ('Player Transfer', 'Player Transfer'),

        ('Fine', 'Fine'),

        ('Sponsorship', 'Sponsorship'),

        ('Match Revenue', 'Match Revenue'),

        ('Expense', 'Expense'),

    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField()

    transaction_date = models.DateField()

    approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.category} - {self.amount}"