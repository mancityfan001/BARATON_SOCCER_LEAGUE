from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Complaint
from notifications.models import AdminNotification


@login_required
def submit_complaint(request):
    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        complaint = Complaint.objects.create(
            coach=request.user,
            subject=subject,
            message=message
        )

        # Notify admin
        AdminNotification.objects.create(
            title="New Complaint",
            message=f"{request.user.username} submitted a complaint: {subject}"
        )

        return redirect('/dashboard/')

    return render(request, 'complaints/submit_complaint.html')