from django.shortcuts import render
from rest_framework import viewsets
from Support_API import models
from . import serializers


class ProjectViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.SupportSerializer
    queryset = models.Project.objects.all()
