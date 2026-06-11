from django.db import models
from matches.models import Match


from django.db import models
from teams.models import Team


class Player(models.Model):
    player_name = models.CharField(max_length=100)
    school_id = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    jersey_number = models.IntegerField(default=0)
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    POSITION_CHOICES = (
        ('Goalkeeper', 'Goalkeeper'),
        ('Defender', 'Defender'),
        ('Midfielder', 'Midfielder'),
        ('Forward', 'Forward'),
    )

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='Defender'
    )

    goals = models.IntegerField(default=0)

    assists = models.IntegerField(default=0)

    clean_sheets = models.IntegerField(default=0)

    goal_conceded = models.IntegerField(default=0)

    yellow_cards = models.IntegerField(default=0)
    
    red_cards = models.IntegerField(default=0)

    is_suspended = models.BooleanField(default=False)

    suspension_matches = models.IntegerField(default=0)

    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='players'
    )

    def save(self, *args, **kwargs):

        if self.suspension_matches > 0:
            self.is_suspended = True
        else:
            self.is_suspended = False

        super().save(*args, **kwargs)

    def __str__(self):
        return self.player_name


class Transfer(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    from_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='from_team'
    )

    to_team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='to_team'
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        if self.status == 'Approved':
            pass

    def __str__(self):
        return f"{self.player} -> {self.to_team}"

class TransferPayment(models.Model):

    transfer = models.OneToOneField(
        Transfer,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_code = models.CharField(
        max_length=100
    )

    proof_of_payment = models.FileField(
        upload_to='transfer_payments/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment for {self.transfer.player}"
    
class Card(models.Model):

    CARD_CHOICES = (

        ('Yellow', 'Yellow'),

        ('Red', 'Red'),

    )

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE
    )

    match = models.ForeignKey(
        'matches.Match',
        on_delete=models.CASCADE
    )

    card_type = models.CharField(
        max_length=10,
        choices=CARD_CHOICES
    )

    minute_given = models.IntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        # AUTO CARD TRACKING

        if not hasattr(self.player, 'yellow_cards'):

            self.player.yellow_cards = 0

        if not hasattr(self.player, 'red_cards'):

            self.player.red_cards = 0

        if not hasattr(self.player, 'is_suspended'):

            self.player.is_suspended = False

        # YELLOW CARD

        if self.card_type == 'Yellow':

            self.player.yellow_cards += 1

        # RED CARD

        elif self.card_type == 'Red':

            self.player.red_cards += 1

            self.player.is_suspended = True

        # AUTO SUSPENSION AFTER 2 YELLOWS

        if self.player.yellow_cards >= 2:

            self.player.is_suspended = True

        self.player.save()

    def __str__(self):

        return f"{self.player} - {self.card_type}"