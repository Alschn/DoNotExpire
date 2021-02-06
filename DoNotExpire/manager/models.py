import os
from django.db import models
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
)
from DoNotExpire.profiles.models import Profile
from datetime import timedelta
from django.utils import timezone


alphanumeric = RegexValidator(r'^[0-9a-zA-Z.-_]*', 'Account name should consist of alphanumerics and .-_ signs')
letters_only = RegexValidator(r'^[a-zA-Z]+$', 'Character name should consist of letters only.')


class Account(models.Model):
    name = models.CharField(max_length=15, validators=[alphanumeric, MinLengthValidator(2)], unique=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='accounts')
    REALMS_CHOICES = (
        ('Europe', "Europe"),
        ('US West', "US West"),
        ('US East', "US East"),
        ('Asia', 'Asia'),
    )
    realm = models.CharField(max_length=7, choices=REALMS_CHOICES)
    last_visited = models.DateTimeField(default=None, null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name}  @{self.realm}"


class Character(models.Model):
    name = models.CharField(max_length=15, validators=[letters_only], unique=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])
    CLASS_CHOICES = (
        ('Amazon', 'Amazon'),
        ('Barbarian', 'Barbarian'),
        ('Necromancer', 'Necromancer'),
        ('Paladin', 'Paladin'),
        ('Sorceress', 'Sorceress'),
        ('Druid', 'Druid'),
        ('Assassin', 'Assassin'),
    )
    char_class = models.CharField(choices=CLASS_CHOICES, max_length=11)
    class_image = models.ImageField(blank=True)
    acc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='chars')
    last_visited = models.DateTimeField(null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True)
    expansion = models.BooleanField(default=True, null=True, blank=True)
    hardcore = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.char_class} {self.level}lvl"

    def get_class_image(self):
        for char_choice in self.CLASS_CHOICES:
            if self.char_class in char_choice:
                pic_name = os.path.join("/media", str(self.char_class + ".gif"))
                return pic_name
        return None

    def expires(self):
        expiration_date = self.last_visited + timedelta(days=60)
        days_until = expiration_date - timezone.now()
        return days_until.days
