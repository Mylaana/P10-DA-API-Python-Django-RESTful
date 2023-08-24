from django.shortcuts import render
from rest_framework import viewsets
from Support_API import models
from . import serializers
from rest_framework.authentication import TokenAuthentication


class ProjectViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.ProjectSerializer
    queryset = models.Project.objects.all()
    authentication_classes = (TokenAuthentication,)


class IssueViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.IssueSerializer
    queryset = models.Issue.objects.all()
    authentication_classes = (TokenAuthentication,)


class CommentViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()
    authentication_classes = (TokenAuthentication,)
