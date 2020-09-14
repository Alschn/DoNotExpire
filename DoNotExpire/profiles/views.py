from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Your account has been created! You are now able to login.")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})
