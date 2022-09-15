from django.contrib import messages
from django.shortcuts import render, redirect

from profiles.forms.auth import UserRegisterForm


class RegisterView:
    # TODO
    pass


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created! You are now able to login."
            )
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})
