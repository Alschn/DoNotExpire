from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DeleteView
from django.contrib import messages
from django.utils import timezone
from .forms import CreateAccountForm, CreateCharacterForm
from .models import Account, Character


def home(request):
    """Home page view if user is logged in or not."""
    try:
        user_accounts = request.user.profile.accounts.all()
    except AttributeError:
        user_accounts = None

    context = {
        'user_accounts': user_accounts,
    }
    return render(request, 'manager/index.html', context)


@login_required
def create_char(request, pk):
    """Current user can add a new character to the account
    where he clicked the button to do so."""
    # if current account has 16 chars, then redirect to homepage with message
    # else create form for char creation
    if request.method == "POST":
        c_form = CreateCharacterForm(request.POST)
        if c_form.is_valid():
            if Account.objects.get(name=pk).chars.all().count() >= 16:
                # maybe there will be just redirect to home and message to the user
                messages.warning(request, "Reached max number of characters per account!")
                return redirect('home')
            instance = c_form.save(commit=False)
            instance.acc = Account.objects.get(name=pk)
            instance.class_image = instance.get_class_image()
            instance.save()
            return redirect('home')
    else:
        c_form = CreateCharacterForm()
    return render(request, 'manager/create_char.html', {"c_form": c_form})


@login_required
def create_account(request):
    """Current user can add his accounts."""
    if request.method == "POST":
        a_form = CreateAccountForm(request.POST)
        if a_form.is_valid():
            instance = a_form.save(commit=False)
            instance.profile = request.user.profile
            instance.save()
            return redirect('home')
    else:
        a_form = CreateAccountForm()
    return render(request, 'manager/create_account.html', {"a_form": a_form})


@login_required
def update_date(request, name):
    """Updates character's last_visited datefield."""
    if request.method == "POST":
        char = Character.objects.get(name=name)
        if char.last_visited and char.expires() < 0:
            char.expired = True
            char.save()
            messages.error(request, f"{char.name} has expired :(")
            return redirect('home')
        char.last_visited = timezone.now()
        char.save()
        return redirect('home')

@login_required
def delete_char(request):
    """Delete character working with a button.
    Once the button is clicked, user is asked to confirm their action
    on the modal that popped up."""
    if 'char_id' in request.POST:
        try:
            char = Character.objects.get(name=request.POST.get('char_id'))
            char.delete()
            messages.success(request, f"{char.name} from account {char.acc} has been deleted")
        except ObjectDoesNotExist:
            messages.warning(request, "Select a character to be deleted first!")
            return redirect('home')
    return redirect('home')


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Account
    success_url = '/'
    template_name = 'manager/delete_account.html'

    def test_func(self):
        """Checks if current user is the creator of this account."""
        acc = self.get_object()
        if acc in self.request.user.profile.accounts.all():
            return True
        return False
