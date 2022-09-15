from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from manager.forms.character import CreateCharacterForm
from manager.models import Account

MAXIMUM_CHARACTERS_PER_ACCOUNT = 18


class CharacterCreateView(LoginRequiredMixin, generic.CreateView):
    """Current user can add a new character to the account
    where he clicked the button to do so. User can have up to 18 characters.
    """

    model = Account
    form_class = CreateCharacterForm
    template_name = 'manager/character_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object is None:
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Account]:
        return Account.objects.filter(profile__user=self.request.user)

    def get_object(self, *args, **kwargs) -> Account | None:
        queryset = self.get_queryset()
        return queryset.filter(name=self.kwargs['name']).first()

    def form_valid(self, form: CreateCharacterForm) -> HttpResponseRedirect:
        if self.get_object().get_all_characters_count() >= MAXIMUM_CHARACTERS_PER_ACCOUNT:
            messages.warning(self.request, "Reached max number of characters per account!")
            return redirect('home')

        instance = form.save(commit=False)
        instance.acc = self.get_object()
        acc = instance.acc
        acc.last_visited = timezone.now()
        acc.save(update_fields=['last_visited'])
        instance.save()
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse('home')
