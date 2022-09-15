from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from manager.models import Account


class AccountDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Confirm that you want to delete selected account"""

    model = Account
    success_url = reverse_lazy('home')
    template_name = 'manager/account_delete.html'

    def test_func(self) -> bool:
        """Checks if current user is the creator of this account."""

        acc = self.get_object()
        if acc in self.request.user.profile.accounts.all():
            return True
        return False
