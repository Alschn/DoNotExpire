from django.core.validators import (
    MinLengthValidator,
)
from django.db import models
from django.utils import timezone

from manager.validators import alphanumeric_validator


class Account(models.Model):
    class Realm(models.TextChoices):
        EUROPE = "Europe", "Europe"
        US_WEST = "US West", "US West"
        US_EAST = "US East", "US East"
        ASIA = "Asia", "Asia"

    name = models.CharField(
        max_length=15,
        validators=[alphanumeric_validator, MinLengthValidator(2)],
        unique=True
    )
    profile = models.ForeignKey(
        'profiles.Profile', on_delete=models.CASCADE, related_name='accounts'
    )
    realm = models.CharField(max_length=7, choices=Realm.choices)
    last_visited = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}  @{self.realm}"

    def get_all_characters(self):
        return self.chars.all()

    def get_all_characters_count(self) -> int:
        return self.chars.all().count()

    class Meta:
        ordering = ['id']
