from DoNotExpire.manager.models import Character, Equipment
from DoNotExpire.manager.serializers import EquipmentSerializer
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class IsCharOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            charname = view.kwargs['charname']
            char = Character.objects.get(name=charname)
            if char in request.user.profile.get_all_characters():
                return True
            return False
        except Exception:
            return False


class GetEquipment(APIView):
    permission_classes = [IsAuthenticated | IsCharOwnerPermission]
    serializer_class = EquipmentSerializer

    def get(self, request, charname):
        char = Character.objects.get(name=charname)
        eq = Equipment.objects.filter(char=char)
        if not eq.exists():
            return Response({'Error': f"{charname}'s equipment not found!"}, status=status.HTTP_404_NOT_FOUND)

        eq_json = self.serializer_class(eq.first())
        return Response(eq_json.data, status=status.HTTP_200_OK)


class UpdateEquipment(APIView):
    permission_classes = [IsAuthenticated | IsCharOwnerPermission]
    serializer_class = EquipmentSerializer

    def post(self, request, charname):
        char = Character.objects.filter(name=charname)
        if not char.exists():
            return Response({'Error': 'Received incorrect charname!'}, status=status.HTTP_404_NOT_FOUND)
        char = char.first()
        # Link received data with a character model
        request.data._mutable = True
        request.data['char'] = char.pk
        request.data._mutable = False

        serializer = self.serializer_class(
            instance=char.equipment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(char=char)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Error': 'Invalid serializer data!'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateCharacter(APIView):
    pass


class DeleteCharacter(APIView):
    pass
