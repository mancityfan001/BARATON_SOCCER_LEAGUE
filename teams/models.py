from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model
from django.conf import settings
from baraton_soccer_league import settings

class Team(models.Model):

    CATEGORY_CHOICES = (
        ('Men', 'Men'),
        ('Ladies', 'Ladies'),
    )
    
    name = models.CharField(max_length=100)

    coach = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    limit_choices_to={'role': 'coach'}
)

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='Men'
    )

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

    payment_proof =models.ImageField(
        upload_to='payment_proofs/',
        blank=True,
        null=True
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
    
    from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

User = get_user_model()

def referee_login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        license_number = request.POST.get('license_number')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.save()

        return redirect('/referee-login/')

    return render(request, 'teams/referee_login.html')

class RefereeProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    full_name = models.CharField(max_length=100)

    license_number = models.CharField(
        max_length=50,
        unique=True
    )

    phone_number = models.CharField(max_length=20)

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name