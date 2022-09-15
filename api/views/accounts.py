from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from manager.models import Account
from manager.serializers.account import (
    AccountSerializer, CreateAccountSerializer, UpdateAccountSerializer
)


class AccountsViewSet(ModelViewSet):
    """
    GET     api/accounts/              - list all accounts
    POST    api/accounts/              - create new account
    GET     api/accounts/<str:name>/   - retrieve account
    PUT     api/accounts/<str:name>/   - update account
    PATCH   api/accounts/<str:name>/   - partially update account
    DELETE  api/accounts/<str:name>/   - delete account
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    lookup_field = 'name'

    def get_queryset(self) -> QuerySet[Account]:
        return Account.objects.filter(profile__user=self.request.user)

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return CreateAccountSerializer
        elif hasattr(self, 'action') and self.action in ['update', 'partial_update']:
            return UpdateAccountSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer) -> None:
        serializer.save(profile=self.request.user.profile)

    def perform_update(self, serializer) -> None:
        serializer.save(profile=self.request.user.profile)
