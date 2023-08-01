from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render, redirect

from profiles.forms.auth import UserRegisterForm

REGISTER_SUCCESS_MESSAGE = "Your account has been created! You are now able to login."


def register(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, REGISTER_SUCCESS_MESSAGE)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'profiles/register.html', {'form': form})
