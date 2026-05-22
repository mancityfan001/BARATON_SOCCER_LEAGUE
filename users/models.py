from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = (

        ('admin', 'Admin'),

        ('coach', 'Coach'),

        ('referee', 'Referee'),

    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='coach'
    )

    def __str__(self):

        return self.username