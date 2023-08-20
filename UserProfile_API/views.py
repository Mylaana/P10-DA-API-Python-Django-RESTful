from django.shortcuts import render
from rest_framework import viewsets
from UserProfile_API import models
from . import serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
