from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from manager.forms.account import CreateAccountForm


class AccountsCreateView(LoginRequiredMixin, generic.CreateView):
    """Current user can add his accounts."""

    form_class = CreateAccountForm
    template_name = 'manager/account_create.html'

    def form_valid(self, form: CreateAccountForm) -> HttpResponseRedirect:
        form.instance.profile = self.request.user.profile
        form.instance.last_visited = timezone.now()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('home')
