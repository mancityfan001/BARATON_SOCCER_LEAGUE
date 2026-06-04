from django.db import models
from django.conf import settings


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

    coach = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
    )

    transfer = models.ForeignKey(
        'players.Transfer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    transaction_code = models.CharField(
    max_length=50,
    blank=True
    )

    payment_proof = models.ImageField(
    upload_to='payment_proofs/',
    null=True,
    blank=True
    )

    status = models.CharField(
    max_length=20,
    choices=(
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ),
     default='Pending'
)

def __str__(self):

        return f"{self.category} - {self.amount}"