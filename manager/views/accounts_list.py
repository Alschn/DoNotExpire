from django.db.models import QuerySet
from django.views import generic

from manager.models import Account


class AccountsListView(generic.ListView):
    """List all accounts accessible to the current user or empty page otherwise."""

    model = Account
    template_name = 'manager/index.html'
    context_object_name = 'user_accounts'

    def get_queryset(self) -> QuerySet[Account]:
        if not self.request.user.is_authenticated:
            return Account.objects.none()

        return self.request.user.profile.accounts.all()
