from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile - {self.created.strftime('%d/%m/%Y-%H:%M')}"

    def get_all_accounts(self):
        return self.accounts.all()

    def get_accounts_count(self) -> int:
        return self.get_all_accounts().count()

    def get_all_characters(self) -> list:
        chars = []
        for acc in self.get_all_accounts():
            # join two lists by unpacking
            chars = [*chars, *acc.get_all_characters()]
        return chars

    def get_all_expired_characters(self) -> list:
        chars = list(filter(lambda char: char.expired, self.get_all_characters()))
        return chars

    def get_all_characters_count(self) -> int:
        count = 0
        for acc in self.get_all_accounts():
            count += acc.get_all_characters_count()
        return count
