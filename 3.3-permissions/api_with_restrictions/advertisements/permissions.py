from rest_framework.permissions import BasePermission


class IsOwnerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        return obj.creator == request.user
