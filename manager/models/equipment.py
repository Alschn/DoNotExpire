from django.db import models


class Equipment(models.Model):
    char = models.OneToOneField('manager.Character', on_delete=models.CASCADE)
    helmet = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    armor = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    belt = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    gloves = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    boots = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    amulet = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    left_ring = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    right_ring = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    main_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    off_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    switch_main_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    switch_off_hand = models.CharField(
        default=None, null=True, blank=True, max_length=50
    )
    torch = models.CharField(
        default=None, null=True, blank=True, max_length=10
    )
    anni = models.CharField(
        default=None, null=True, blank=True, max_length=10
    )
    charms = models.CharField(
        default=None, null=True, blank=True, max_length=100
    )

    def __str__(self) -> str:
        return f"{self.char.name}'s equipment"
