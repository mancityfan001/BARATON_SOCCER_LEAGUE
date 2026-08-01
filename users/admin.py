from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (

        'username',

        'email',
        
        'phone_number',

        'role',

        'admin_approved',

        'is_staff',

        'is_superuser',

    )

    actions = ['approve_admins']

    def approve_admins(self, request, queryset):
        queryset.filter(
            role='admin',
            admin_approved=False
        ).update(
            admin_approved=True,
            is_staff=True
        )

    approve_admins.short_description = "Approve selected administrators"