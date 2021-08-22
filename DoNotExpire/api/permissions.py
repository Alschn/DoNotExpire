from rest_framework import permissions

from DoNotExpire.manager.models import Character, Account


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


class IsCharOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.acc.profile.user
        return True


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.profile.user
        elif request.method == 'POST':
            return request.user.profile == obj.profile
        return True
