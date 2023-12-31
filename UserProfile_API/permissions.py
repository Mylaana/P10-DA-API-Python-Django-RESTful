from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.id == request.user.id or request.user.is_admin:
            return True

        return False
