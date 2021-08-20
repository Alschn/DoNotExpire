from rest_framework import permissions

from DoNotExpire.manager.models import Character


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
