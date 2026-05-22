from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ROLE REDIRECTION

            if user.role == 'admin':

                return redirect('/admin/')

            elif user.role == 'coach':

                return redirect('coach_dashboard')

            elif user.role == 'referee':

                return redirect('referee_dashboard')

        else:

            messages.error(
                request,
                'Invalid username or password'
            )

    return render(
        request,
        'users/login.html'
    )