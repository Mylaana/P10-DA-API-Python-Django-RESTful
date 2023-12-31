from rest_framework import permissions
from Support_API import models

class UpdateRessource(permissions.BasePermission):
    """Allow user to edit a ressource"""
    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin or request.user.is_superuser:
            return True

        if not self.is_project_contributor(request, obj):
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if self.is_project_author(request, obj):
            return True

        return False

    def is_project_contributor(self, request, obj):
        """
        returning True if request.user is amongst contributors
        """
        contributors = None
        if isinstance(obj, models.Project):
            contributors = obj.contributors.all()
        elif isinstance(obj, models.Issue):
            contributors = obj.project.contributors.all()
        elif isinstance(obj, models.Comment):
            contributors = obj.issue.project.contributors.all()

        for contributor in contributors:
            if contributor.user_profile == request.user:
                return True

        return False

    def is_project_author(self, request, obj):
        """
        returning True if request.user is project's author
        """
        return obj.author.user_profile == request.user


class UpdateContribution(permissions.BasePermission):
    """Allow user to edit a ressource"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin or request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        return False
