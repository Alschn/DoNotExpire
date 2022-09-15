from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile - {self.created.strftime('%d/%m/%Y-%H:%M')}"

    def get_all_accounts(self) -> QuerySet:
        return self.accounts.all()

    def get_all_accounts_count(self) -> int:
        return self.get_all_accounts().count()

    def get_all_characters(self) -> QuerySet:
        from manager.models import Character
        return Character.objects.filter(acc__profile__user=self.user)

    def get_all_expired_characters(self) -> QuerySet:
        return self.get_all_characters().filter(expired=True)

    def get_all_characters_count(self) -> int:
        return self.get_all_characters().count()
