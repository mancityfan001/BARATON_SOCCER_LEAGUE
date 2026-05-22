from django.contrib import admin
from .models import FinanceRecord


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):

    list_display = (

        'category',

        'team',

        'amount',

        'transaction_date',

        'approved',

    )

    list_filter = (

        'category',

        'approved',

    )