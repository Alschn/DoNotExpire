from rest_framework import serializers

from .models import Account, Equipment, Character


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    char = CharacterSerializer(read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'


class CharacterBumpSerializer(serializers.ModelSerializer):
    expires_in = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = '__all__'

    def get_expires_in(self, obj):
        return obj.expires()
