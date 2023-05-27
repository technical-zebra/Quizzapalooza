from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegistrationForm


def login_view(request):
    """
    This function handles the login process by checking the user's email and password, and if they
    match, logs the user in and redirects them to the home page.
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    login(request, user)
                    messages.success(request, 'Login successful!')
                    return redirect('home')
                else:
                    messages.error(request, 'Incorrect password!')
            else:
                messages.error(request, 'User does not exist!')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    """
    This function logs out the user and redirects them to the login page.
    """
    logout(request)
    return redirect('/login')


def register_view(request):
    """
    This function handles the registration process for a user, checking for valid email and password
    requirements before creating a new user account.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password and confirm_password and password != confirm_password:
                messages.error(request, "Passwords do not match!")

            else:
                user = User.objects.filter(email=email).first()
                if user:
                    messages.error(request, 'Email already exists')
                else:
                    new_user = User.objects.create_user(username=email, email=email, password=password)
                    login(request, new_user)
                    messages.success(request, 'Account created!')
                    return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
