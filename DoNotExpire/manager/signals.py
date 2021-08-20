from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Character, Equipment


@receiver(post_save, sender=Character)
def create_equipment(sender, instance, created, **kwargs):
    if created:
        Equipment.objects.create(char=instance)


@receiver(post_save, sender=Character)
def save_equipment(sender, instance, created, **kwargs):
    instance.equipment.save()
