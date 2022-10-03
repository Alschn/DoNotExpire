from rest_framework import serializers

from manager.models import Account, Character


class AccountForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        if self.context.get('request'):
            return Account.objects.filter(profile__user=self.context['request'].user)
        return super().get_queryset()


class CharacterSerializer(serializers.ModelSerializer):
    acc = AccountForeignKey(read_only=True)

    class Meta:
        model = Character
        fields = (
            'id', 'name', 'level', 'char_class', 'acc',
            'last_visited', 'expired', 'expansion', 'hardcore', 'ladder',
        )


class CreateCharacterSerializer(CharacterSerializer):
    last_visited = serializers.DateTimeField(read_only=True)
    expired = serializers.BooleanField(read_only=True)
    acc = AccountForeignKey(required=True)


class UpdateCharacterSerializer(CharacterSerializer):
    last_visited = serializers.DateTimeField(required=False)
    expired = serializers.BooleanField(required=False)
    # not possible to change character's name
    name = serializers.CharField(read_only=True)


class CharacterBumpSerializer(serializers.ModelSerializer):
    expires_in = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = (
            'id', 'name', 'level', 'char_class', 'acc',
            'last_visited', 'expires_in', 'expired', 'expansion', 'hardcore', 'ladder',
        )

    def get_expires_in(self, obj: Character):
        return obj.expires
