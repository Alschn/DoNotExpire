from django.shortcuts import render
from .forms import CreateAccountForm, CreateCharacterForm


def home(request):
    return render(request, 'manager/index.html')


def create_char(request):
    # c_form = CreateCharacterForm()
    return render(request, 'manager/create_char.html')


def create_account(request):
    # a_form = CreateAccountForm()
    return render(request, 'manager/create_char.html')
