from django.shortcuts import render, redirect, reverse
from django.utils import timezone
import datetime
from .forms import CreateAccountForm, CreateCharacterForm
from .models import Character


def home(request):
    user_accounts = request.user.profile.accounts.all()

    context = {
        'user_accounts': user_accounts,
    }
    return render(request, 'manager/index.html', context)


def create_char(request):
    # if current account has 16 chars, then redirect to homepage with message
    # else create form for char creation
    if request.method == "POST":
        c_form = CreateCharacterForm(request.POST)
        if c_form.is_valid():
            return redirect('home')
    else:
        c_form = CreateCharacterForm()
    return render(request, 'manager/create_char.html')


def create_account(request):
    if request.method == "POST":
        c_form = CreateAccountForm(request.POST)
        if c_form.is_valid():
            return redirect('home')
    else:
        c_form = CreateAccountForm()
    return render(request, 'manager/create_acc.html')


def update_date(request, name):
    """Updates character's last_visited datefield."""
    if request.method == "POST":
        char = Character.objects.get(name=name)
        char.last_visited = datetime.datetime.now()
        char.save()
        return redirect('home')


def delete_char(request):
    if request.method == "POST":
        pass
    return redirect('home')
