from rest_framework import serializers
from Support_API import models

class SupportSerializer(serializers.ModelSerializer):
    """Serializes Project model"""

    class Meta:
        model = models.Project
        fields = ('id', 'name')


    def create(self, validated_data):
        """Create and return new user"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=validated_data['author'],
        )

        return project
