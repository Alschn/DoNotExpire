from rest_framework import permissions

from manager.models import Character


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.profile.user
        elif request.method == 'POST':
            return request.user.profile == obj.profile
        return True
