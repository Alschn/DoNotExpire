from django.db.models import QuerySet
from rest_framework import serializers

from manager.models import Account
from profiles.models import Profile


class ProfileForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self) -> QuerySet[Profile]:
        if request := self.context.get('request'):
            return Profile.objects.filter(user=request.user)

        return super().get_queryset()


class AccountSerializer(serializers.ModelSerializer):
    profile = ProfileForeignKey(required=False)

    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'profile',
            'realm',
            'last_visited',
            'expired'
        )


class CreateAccountSerializer(AccountSerializer):
    last_visited = serializers.DateTimeField(read_only=True)
    expired = serializers.BooleanField(read_only=True)


class UpdateAccountSerializer(AccountSerializer):
    name = serializers.CharField(read_only=True)  # not possible to change accounts' name
