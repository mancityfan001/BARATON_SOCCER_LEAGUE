from django.contrib import admin
from .models import FinanceRecord
from players.models import Transfer, TransferPayment


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):

    list_display = (
        'category',
        'player' ,
        'referee',
        'coach',
        'team',
        'amount',
        'transaction_date',
        'status',
        'approved',
    )

    list_filter = (
        'category',
        'approved',
        'status',
    )

    actions = ['approve_transfer_payment']

    def approve_transfer_payment(self, request, queryset):

        for record in queryset:

            if record.category == 'Player Transfer':

                record.approved = True
                record.status = 'Approved'
                record.save()

                if record.transfer:

                    transfer = record.transfer

                    transfer.status = 'Approved'
                    transfer.save()

                    player = transfer.player
                    player.team = transfer.to_team
                    player.save()

                    try:
                        payment = TransferPayment.objects.get(
                            transfer=transfer
                        )
                        payment.status = 'Approved'
                        payment.save()

                    except TransferPayment.DoesNotExist:
                        pass

    approve_transfer_payment.short_description = (
        "Approve selected transfer payments"
    )