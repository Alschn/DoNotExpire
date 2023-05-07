from datetime import timedelta

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils import timezone

from manager.validators import letters_only_validator, underscore_validator


class Character(models.Model):
    class Class(models.TextChoices):
        AMAZON = 'Amazon', 'Amazon'
        BARBARIAN = 'Barbarian', 'Barbarian'
        NECROMANCER = 'Necromancer', 'Necromancer'
        PALADIN = 'Paladin', 'Paladin'
        SORCERESS = 'Sorceress', 'Sorceress'
        DRUID = 'Druid', 'Druid'
        ASSASSIN = 'Assassin', 'Assassin'

    name = models.CharField(
        max_length=15,
        validators=[letters_only_validator, underscore_validator],
        unique=True
    )
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
    char_class = models.CharField(choices=Class.choices, max_length=11)
    acc = models.ForeignKey('manager.Account', on_delete=models.CASCADE, related_name='chars')
    last_visited = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)
    expansion = models.BooleanField(default=True, null=True, blank=True)
    hardcore = models.BooleanField(default=False, null=True, blank=True)
    ladder = models.BooleanField(default=False, blank=True)

    def __str__(self) -> str:
        return f"{self.name}: {self.char_class} {self.level}lvl"

    def get_class_image(self) -> str | None:
        for char_choice in self.Class.choices:
            if self.char_class in char_choice:
                pic_name = str(self.char_class + ".gif").lower()
                return f"manager/images/{pic_name}"
        return None

    def update_last_visited(self) -> None:
        self.last_visited = timezone.now()
        self.save(update_fields=['last_visited'])

    def update_expired(self) -> None:
        self.expired = self.expires < 0
        self.save(update_fields=['expired'])

    @property
    def expires(self) -> int:
        expiration_date = self.last_visited + timedelta(days=90)
        days_until = expiration_date - timezone.now()
        return days_until.days

    class Meta:
        ordering = ['id']
