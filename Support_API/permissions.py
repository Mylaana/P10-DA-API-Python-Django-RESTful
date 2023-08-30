from rest_framework import permissions

class UpdateRessource(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_admin or request.user.is_superuser:
            return True

        if request.method == 'DELETE' :
            return False

        return True
