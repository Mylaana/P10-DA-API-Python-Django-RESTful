from rest_framework import viewsets
from Support_API import models
from . import serializers
from rest_framework.permissions import IsAuthenticated
from Support_API import permissions


class ProjectViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]


class IssueViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]

    def get_queryset(self):
        project_id=self.kwargs['project_id']
        return self.queryset.filter(project_id=project_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]

    def get_queryset(self):
        issue_id=self.kwargs['issue_id']
        return self.queryset.filter(issue_id=issue_id)

class ContributionViewSet(viewsets.ModelViewSet):
    """Handles user contribution to projects"""
    serializer_class = serializers.ContributionSerializer
    queryset = models.ContributorProjet.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]

    def get_queryset(self):
        contributors=3
        return self.queryset.filter(contributors=contributors)