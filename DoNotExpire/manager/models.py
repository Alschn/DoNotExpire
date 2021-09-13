from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
)
from django.db import models
from django.utils import timezone

from DoNotExpire.profiles.models import Profile

alphanumeric = RegexValidator(
    r'^[0-9a-zA-Z\.\-\_]{2,15}$',
    'Account name should consist of alphanumerics and ".", "-", "_" signs, and be between 2 and 15 characters.'
)  # and probably more special signs

letters_only = RegexValidator(
    r'^[a-zA-Z\_]{2,15}$',
    "Character's name should consist of letters only and up to one underscore. It should be between 2 and 15 "
    "characters. "
)


def underscore_validator(value: str):
    if value.count('_') > 1:
        raise ValidationError(
            "Character's name can consist of at most one underscore!"
        )
    elif value.startswith('_') or value.endswith('_'):
        raise ValidationError(
            "Character's name cannot start nor end with an underscore!"
        )


class Account(models.Model):
    name = models.CharField(
        max_length=15,
        validators=[alphanumeric, MinLengthValidator(2)],
        unique=True
    )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='accounts'
    )
    REALMS_CHOICES = (
        ('Europe', "Europe"),
        ('US West', "US West"),
        ('US East', "US East"),
        ('Asia', 'Asia'),
    )
    realm = models.CharField(max_length=7, choices=REALMS_CHOICES)
    last_visited = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expired = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.name}  @{self.realm}"

    def get_all_characters(self):
        return self.chars.all()

    def get_all_characters_count(self):
        return self.chars.all().count()

    class Meta:
        ordering = ['id']


class Character(models.Model):
    name = models.CharField(
        max_length=15,
        validators=[letters_only, underscore_validator],
        unique=True
    )
    level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )
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
    acc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='chars')
    last_visited = models.DateTimeField(default=timezone.now)
    expired = models.BooleanField(default=False)
    expansion = models.BooleanField(default=True, null=True, blank=True)
    hardcore = models.BooleanField(default=False, null=True, blank=True)
    ladder = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f"{self.name}: {self.char_class} {self.level}lvl"

    def get_class_image(self):
        for char_choice in self.CLASS_CHOICES:
            if self.char_class in char_choice:
                pic_name = str(self.char_class + ".gif").lower()
                return pic_name
        return None

    def expires(self):
        expiration_date = self.last_visited + timedelta(days=90)
        days_until = expiration_date - timezone.now()
        return days_until.days

    class Meta:
        ordering = ['id']


class Equipment(models.Model):
    char = models.OneToOneField(Character, on_delete=models.CASCADE)
    helmet = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    armor = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    belt = models.CharField(default=None, null=True, blank=True, max_length=50)
    gloves = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    boots = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    amulet = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    left_ring = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    right_ring = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    main_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    off_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    switch_main_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    switch_off_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50)
    torch = models.CharField(default=None, null=True,
                             blank=True, max_length=10)
    anni = models.CharField(default=None, null=True, blank=True, max_length=10)
    charms = models.CharField(default=None, null=True,
                              blank=True, max_length=100)

    def __str__(self) -> str:
        return f"{self.char.name}'s equipment"
