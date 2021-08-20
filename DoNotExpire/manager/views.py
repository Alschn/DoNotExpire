from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import DeleteView

from .forms import CreateAccountForm, CreateCharacterForm
from .models import Account, Character


def home(request):
    """Home page view if user is logged in or not."""
    if request.user.is_authenticated:
        user_accounts = request.user.profile.accounts.all()
    else:
        user_accounts = None

    return render(request, 'manager/index.html', {'user_accounts': user_accounts})


@login_required
def create_char(request, acc_name, **kwargs):
    """Current user can add a new character to the account
    where he clicked the button to do so. User can have up to 18 characters.
    """
    # if current account has 18 chars, then redirect to homepage with message
    # else create form for char creation
    if request.method == "POST":
        c_form = CreateCharacterForm(request.POST)
        if c_form.is_valid():
            if Account.objects.get(name=acc_name).chars.all().count() >= 18:
                messages.warning(request, "Reached max number of characters per account!")
                return redirect('home')
            instance = c_form.save(commit=False)
            instance.acc = Account.objects.get(name=acc_name)
            acc = instance.acc
            acc.last_visited = timezone.now()
            acc.save()
            instance.save()
            return redirect('home')
    else:
        c_form = CreateCharacterForm()
    return render(request, 'manager/create_char.html', {"c_form": c_form})


@login_required
def create_account(request, *args, **kwargs):
    """Current user can add his accounts."""
    if request.method == "POST":
        a_form = CreateAccountForm(request.POST)
        if a_form.is_valid():
            instance = a_form.save(commit=False)
            instance.profile = request.user.profile
            instance.last_visited = timezone.now()
            instance.save()
            return redirect('home')
    else:
        a_form = CreateAccountForm()
    return render(request, 'manager/create_account.html', {"a_form": a_form})


@login_required
def update_date(request, char_name, **kwargs):
    """Updates character's last_visited date field.
    Not used anymore (replaced with api view).
    """
    if request.method == "POST":
        char = Character.objects.get(name=char_name)
        acc = char.acc
        if char.last_visited and char.expires() < 0:
            char.expired = True
            char.save()
            messages.error(request, f"{char.name} has expired :(")
            return redirect('home')
        char.last_visited = timezone.now()
        acc.last_visited = timezone.now()
        char.save()
        acc.save()
        messages.success(request, f"You have just visited {char.name} and refreshed their expiration date!")
        return redirect('home')


@login_required
def delete_char(request, *args, **kwargs):
    """Delete character working with a button.
    Once the button is clicked, user is asked to confirm their action
    on the modal that popped up.
    Not used anymore (replaced with api view).
    """
    if 'char_id' in request.POST:
        try:
            char = Character.objects.get(name=request.POST.get('char_id'))
            acc = char.acc
            acc.last_visited = timezone.now()
            acc.save()
            char.delete()
            messages.success(request, f"{char.name} from account {char.acc} has been deleted")
        except ObjectDoesNotExist:
            messages.warning(request, "Select a character to be deleted first!")
            return redirect('home')
    return redirect('home')


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Confirm that you want to delete selected account"""
    model = Account
    success_url = '/'
    template_name = 'manager/delete_account.html'

    def test_func(self):
        """Checks if current user is the creator of this account."""
        acc = self.get_object()
        if acc in self.request.user.profile.accounts.all():
            return True
        return False
