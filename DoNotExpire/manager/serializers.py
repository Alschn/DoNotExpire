from rest_framework import serializers

from .models import Account, Equipment, Character
from ..profiles.models import Profile


class ProfileForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        if self.context.get('request'):
            return Profile.objects.filter(user=self.context['request'].user)
        return super().get_queryset()


class AccountForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        if self.context.get('request'):
            return Account.objects.filter(profile__user=self.context['request'].user)
        return super().get_queryset()


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileForeignKey(required=False)

    class Meta:
        model = Account
        fields = '__all__'


class CreateAccountSerializer(AccountSerializer):
    last_visited = serializers.DateTimeField(read_only=True)
    expired = serializers.BooleanField(read_only=True)


class UpdateAccountSerializer(AccountSerializer):
    # not possible to change accounts's name
    name = serializers.CharField(read_only=True)


class CharacterSerializer(serializers.ModelSerializer):
    acc = AccountForeignKey(read_only=True)

    class Meta:
        model = Character
        fields = '__all__'


class CreateCharacterSerializer(CharacterSerializer):
    last_visited = serializers.DateTimeField(read_only=True)
    expired = serializers.BooleanField(read_only=True)
    acc = AccountForeignKey(required=True)


class UpdateCharacterSerializer(CharacterSerializer):
    last_visited = serializers.DateTimeField(required=False)
    expired = serializers.BooleanField(required=False)
    # not possible to change character's name
    name = serializers.CharField(read_only=True)


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
        return obj.expires
