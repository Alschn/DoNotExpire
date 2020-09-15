from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator,
    MinLengthValidator,
    FileExtensionValidator
)
from DoNotExpire.profiles.models import Profile


alphanumeric = RegexValidator(r'^[0-9a-zA-Z.-]*', 'Account name should consist of alphanumerics and .- signs')
letters_only = RegexValidator(r'^[a-zA-Z]*', 'Character name should consist of letters only.')


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

    def save(self, *args, **kwargs):
        # something like this to limit character count per account?
        max_char_count_per_acc = 16
        if self.account.chars.all().count() >= max_char_count_per_acc:
            raise ValidationError(
                'You can have up to 16 characters per account in Diablo II.'
            )
        super().save(*args, **kwargs)


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

    def __str__(self):
        return f"{self.name}: {self.char_class} {self.level}lvl"

    def get_class_image(self):
        for char_choice in self.CLASS_CHOICES:
            if self.char_class in char_choice:
                pic_name = str(self.char_class + ".jpg")
                return pic_name
        return None
