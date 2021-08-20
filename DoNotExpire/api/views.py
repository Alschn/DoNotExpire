from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from DoNotExpire.api.permissions import IsCharOwnerPermission
from DoNotExpire.manager.models import Character, Equipment, Account
from DoNotExpire.manager.serializers import (
    EquipmentSerializer, AccountSerializer,
    CharacterSerializer, CharacterBumpSerializer
)


class CharacterBumpLastVisited(APIView):
    """
    PATCH /api/chars/<str:charname>/bump - update character's last visited field
    (and expired field in case character is expired)
    """
    permission_classes = [IsAuthenticated, IsCharOwnerPermission]

    def patch(self, request, *args, **kwargs):
        char_name = kwargs.get('charname')
        if not char_name:
            return Response(
                {'error': f'Character name missing in url!'},
                status.HTTP_404_NOT_FOUND
            )

        char = Character.objects.filter(name=char_name)
        if not char.exists():
            return Response({'error': f'Character {char_name} does not exist!'}, status.HTTP_404_NOT_FOUND)

        char = char.first()
        acc = char.acc

        # if character expired, set expired to true
        if char.last_visited and char.expires() < 0:
            char.expired = True
            char.save()
            return Response({
                'message': f"{char.name} has expired :(",
                'character': CharacterBumpSerializer(char).data
            }, status.HTTP_200_OK)

        # else bump last_visited fields in char and acc
        char.last_visited = timezone.now()
        acc.last_visited = timezone.now()
        char.save()
        acc.save()
        return Response({
            'message': f"You have just visited {char.name} and refreshed their expiration date!",
            'character': CharacterBumpSerializer(char).data
        }, status.HTTP_200_OK)


class CharacterEquipmentView(APIView):
    """
    GET /api/chars/<str:charname>/bump - Retrieve character's equipment
    POST /api/chars/<str:charname>/bump - Update character's equipment (partially)
    """
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsCharOwnerPermission]
    serializer_class = EquipmentSerializer

    def get(self, request, charname):
        char = Character.objects.filter(name=charname)
        if not char.exists():
            return Response({'Error': f"Character {charname} not found!"}, status=status.HTTP_404_NOT_FOUND)
        eq = Equipment.objects.filter(char=char.first())
        if not eq.exists():
            return Response({'Error': f"{charname}'s equipment not found!"}, status=status.HTTP_404_NOT_FOUND)

        eq_json = self.serializer_class(eq.first())
        return Response(eq_json.data, status=status.HTTP_200_OK)

    def post(self, request, charname):
        if not request.data:
            return Response({'Error': 'Received empty request!'}, status=status.HTTP_400_BAD_REQUEST)

        char = Character.objects.filter(name=charname)
        if not char.exists():
            return Response({'Error': f'Character {charname} not found!'}, status=status.HTTP_404_NOT_FOUND)
        char = char.first()

        eq = Equipment.objects.filter(char=char)
        if not eq.exists():
            return Response({'Error': f"{charname}'s equipment' not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            instance=eq.first(), data=request.data, partial=True
        )

        if serializer.is_valid(raise_exception=False):
            serializer.save(char=char)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterViewSet(ModelViewSet):
    """
    GET     api/chars/              - list all characters
    POST    api/chars/              - create new character
    GET     api/chars/<str:name>/   - retrieve character
    PUT     api/chars/<str:name>/   - update character
    PATCH   api/chars/<str:name>/   - partially update character
    DELETE  api/chars/<str:name>/   - delete character
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()
    lookup_field = 'name'


class AccountViewSet(ModelViewSet):
    """
    GET     api/accs/              - list all accounts
    POST    api/accs/              - create new account
    GET     api/accs/<str:name>/   - retrieve account
    PUT     api/accs/<str:name>/   - update account
    PATCH   api/accs/<str:name>/   - partially update account
    DELETE  api/accs/<str:name>/   - delete account
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = 'name'

# to do - add isOwner permission to both views and write unit tests
