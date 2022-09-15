from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render


class ProfileView:
    # TODO
    pass



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
        request, 'profiles/templates/profiles/profile.html',
        {'profile': profile_, 'accounts': accounts, 'paged_accounts': paged_accounts}
    )
