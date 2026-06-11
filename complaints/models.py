from django.db import models
from users.models import CustomUser


class Complaint(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    )

    coach = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=200)

    message = models.TextField()

    admin_response = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject