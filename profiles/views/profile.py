from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render


@login_required
def profile(request: WSGIRequest) -> HttpResponse:
    profile_ = request.user.profile
    accounts = profile_.accounts.all()

    page_by = 2
    paginator = Paginator(accounts, page_by)
    page_number = request.GET.get('page')
    paged_accounts = paginator.get_page(page_number) if accounts else None

    return render(
        request, 'profiles/profile.html',
        {'profile': profile_, 'accounts': accounts, 'paged_accounts': paged_accounts}
    )
