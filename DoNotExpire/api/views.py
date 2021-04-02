from DoNotExpire.manager.models import Character, Equipment
from DoNotExpire.manager.serializers import EquipmentSerializer
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class IsCharOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if "charname" in view.kwargs:
            charname = view.kwargs['charname']
            char = Character.objects.filter(name=charname)
            if not char.exists():
                # permission is granted
                # errors are handled inside the api view
                return True
            if not char.first() in request.user.profile.get_all_characters():
                return False
        return True


class GetEquipment(APIView):
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


class UpdateEquipment(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsCharOwnerPermission]
    serializer_class = EquipmentSerializer

    def post(self, request, charname):
        char = Character.objects.filter(name=charname)
        if not char.exists():
            return Response({'Error': f'Character {charname} not found!'}, status=status.HTTP_404_NOT_FOUND)
        char = char.first()
        eq = Equipment.objects.filter(char=char)
        if not eq.exists():
            return Response({'Error': f"{charname}'s equipment' not found!"}, status=status.HTTP_404_NOT_FOUND)
        # Link received data with a character model
        request.data._mutable = True
        request.data['char'] = char.pk
        request.data._mutable = False

        serializer = self.serializer_class(
            instance=eq.first(), data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(char=char)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCharacter(APIView):
    pass


class DeleteCharacter(APIView):
    pass
