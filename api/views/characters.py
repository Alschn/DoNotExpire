from typing import Any

from django.db import transaction
from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from manager.models import Character, Equipment
from manager.serializers.character import (
    CharacterSerializer,
    CreateCharacterSerializer,
    UpdateCharacterSerializer,
    CharacterBumpSerializer
)
from manager.serializers.equipment import EquipmentSerializer


class CharactersViewSet(viewsets.ModelViewSet):
    """
    GET     api/characters/                  - list all characters
    POST    api/characters/                  - create new character
    GET     api/characters/<str:name>/       - retrieve character
    PUT     api/characters/<str:name>/       - update character
    PATCH   api/characters/<str:name>/       - partially update character
    DELETE  api/characters/<str:name>/       - delete character

    PATCH   /api/characters/<str:name>/bump/ - update character's last visited field
                                            (and expired field if character is expired)

    GET     /api/characters/<str:name>/equipment/ - retrieve character's equipment
    POST    /api/characters/<str:name>/equipment/ - update character's equipment
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CharacterSerializer
    lookup_field = 'name'

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'create':
            return CreateCharacterSerializer
        elif hasattr(self, 'action') and self.action in ['update', 'partial_update']:
            return UpdateCharacterSerializer
        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[Character]:
        return Character.objects.filter(acc__profile__user=self.request.user)

    def create(self, request: Request, *args, **kwargs) -> Response:
        account_id = request.data.get('acc')
        user_accounts = request.user.profile.get_all_accounts()

        if not user_accounts.filter(id=account_id).exists():
            return Response({'message': 'You do not own this account!'}, status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    def perform_update(self, serializer: UpdateCharacterSerializer) -> None:
        character = self.get_object()
        serializer.save(acc=character.acc)

    @transaction.atomic
    @action(
        detail=True, methods=['PATCH'], url_name='bump',
        permission_classes=[IsAuthenticated]
    )
    def bump(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        character = self.get_object()
        account = character.acc

        # if character expired, set expired to true
        if character.last_visited and character.expires < 0:
            character.update_expired()
            return Response({
                'message': f"{character.name} has expired :(",
                'character': CharacterBumpSerializer(character).data
            }, status=status.HTTP_200_OK)

        # else bump last_visited fields in char and account
        account.update_last_visited()
        character.update_last_visited()

        return Response({
            'message': f"You have just visited {character.name} and refreshed their expiration date!",
            'character': CharacterBumpSerializer(character).data
        }, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['GET', 'POST'], url_name='equipment',
        authentication_classes=[BasicAuthentication, SessionAuthentication]
    )
    def equipment(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        character = self.get_object()

        # If equipment was not created or got deleted for some reason - not allowed by business logic
        if not Equipment.objects.filter(char=character).exists():
            return Response({'message': 'Character has no equipment'}, status=status.HTTP_404_NOT_FOUND)

        equipment = character.equipment

        if request.method == 'POST':
            serializer = EquipmentSerializer(
                instance=equipment,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(char=character)
            return Response(serializer.data, status=status.HTTP_200_OK)

        data = EquipmentSerializer(instance=equipment).data
        return Response(data, status=status.HTTP_200_OK)
