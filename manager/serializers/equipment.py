from rest_framework import serializers

from manager.models import Equipment
from manager.serializers.character import CharacterSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    char = CharacterSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = (
            'id', 'char', 'helmet', 'armor', 'belt', 'gloves',
            'boots', 'amulet', 'left_ring', 'right_ring',
            'main_hand', 'off_hand', 'switch_main_hand',
            'switch_off_hand', 'torch', 'anni', 'charms'
        )
