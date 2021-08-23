from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your account has been created! You are now able to login.")
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})


@login_required
def profile(request):
    profile_ = request.user.profile
    accounts = profile_.accounts.all()

    page_by = 2
    paginator = Paginator(accounts, page_by)
    page_number = request.GET.get('page')
    paged_accounts = paginator.get_page(page_number)

    if not accounts:
        paged_accounts = None
    return render(
        request, 'profiles/profile.html',
        {'profile': profile, 'accounts': accounts, 'paged_accounts': paged_accounts}
    )
