from rest_framework import serializers
from Support_API import models
from UserProfile_API.models import Contributor


def get_contributor(user):
    """
    check if user is already a contributor on any project,
    adds them in contributor list if not

    returns a contributor id
    """

    contributor = Contributor.objects.filter(user_profile=user).first()
    if contributor is None:
        contributor = Contributor.objects.create(user_profile=user)

    return contributor


class ProjectSerializer(serializers.ModelSerializer):
    """Serializes Project model"""

    class Meta:
        model = models.Project
        fields = ('id', 'name')

    def create(self, validated_data):
        """Create and return new user"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
        )

        return project


class IssuSerializer(serializers.ModelSerializer):
    """Serializes Project model"""

    class Meta:
        model = models.Issue
        fields = ('id', 'name', 'project', 'description', 'priority', 'issue_type', 'progression')

    def create(self, validated_data):
        """Create and return new user"""
        issue = models.Issue.objects.create_issue(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
            project=validated_data['project'],
            description=validated_data['description'],
            priority=validated_data['priority'],
            issue_type=validated_data['issue_type'],
            progression=validated_data['progression']
        )

        return issue

class CommentSerializer(serializers.ModelSerializer):
    """Serializes Project model"""

    class Meta:
        model = models.Issue
        fields = ('id', 'name')

    def create(self, validated_data):
        """Create and return new user"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=self.get_contributor(self.context['request'].user),
        )

        return project

    def get_contributor(self, user):
        """
        check if user is already a contributor on any project,
        adds them in contributor list if not

        returns a contributor id
        """

        contributor = Contributor.objects.filter(user_profile=user).first()
        if contributor is None:
            contributor = Contributor.objects.create(user_profile=user)

        return contributor
