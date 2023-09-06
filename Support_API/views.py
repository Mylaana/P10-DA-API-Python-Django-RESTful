from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, pagination 

from Support_API import models
from . import serializers
from Support_API import permissions

def is_contributing(request, project):
    """returns boolean"""
    for contributor in project.contributors.all():
        if request.user.id == contributor.user_profile.id:
            return True
    return False

class ProjectViewSet(viewsets.ModelViewSet):
    """Handle creating and updating project"""
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = models.Project.objects.all()

    def get_queryset(self):
        """customizing queryset according to user rights"""
        if self.request.user.is_admin or self.request.user.is_superuser:
            return models.Project.objects.all()

        contributing_project_list = []
        for project in models.Project.objects.all():
            if is_contributing(request=self.request, project=project):
                contributing_project_list.append(project.id)

        return models.Project.objects.filter(id__in=contributing_project_list)

class IssueViewSet(viewsets.ModelViewSet):
    """Handle creating and updating issues"""
    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]

    def get_queryset(self):
        project_id=self.kwargs['project_id']
        return self.queryset.filter(project_id=project_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # adds project_id to the serializer's context
        context.update({"project_id": self.kwargs.get('project_id')})
        return context

class CommentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating comments"""
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateRessource]

    def get_queryset(self):
        issue_id=self.kwargs['issue_id']

        page_size = self.request.query_params.get('page_size')
        if page_size:
            try:
                page_size = int(page_size)
                if page_size > 0:
                    self.pagination_class.default_limit = page_size
            except ValueError:
                pass  # Ignore si la valeur n'est pas un entier valide

        return self.queryset.filter(issue_id=issue_id)


class ContributionViewSet(viewsets.ModelViewSet):
    """Handles user contribution to projects"""
    serializer_class = serializers.ContributionSerializer
    queryset = models.ContributorProjet.objects.all()
    permission_classes = [IsAuthenticated, permissions.UpdateContribution]

    def list(self, request, *args, **kwargs):
        """customizing the list function to display a project list and no result in serializer's JSON"""
        response = super().list(request, *args, **kwargs)

        data = response.data
        project_list = []
        for project in models.Project.objects.all():
            project_list.append({
                "id": project.id,
                "name": project.name,
                "author": project.author.user_profile.username,
                "creation_date": project.created_time,
                "contributing": is_contributing(request, project)
                })
        data["project_list"] = project_list
        data.pop("results", None)


        response.data = data

        return response

