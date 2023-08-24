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

class BaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    project_id = ""

    def get_url(self, obj):
        request = self.context.get('request', None)
        if request:
            request_url = request.build_absolute_uri()

            if str(request_url.split("/")[-2]) == str(obj.id) :
                return request_url
            else:
                return request_url + self.project_id + str(obj.id) + "/"

class CommentSerializer(serializers.ModelSerializer):
    """Serializes Project model"""

    class Meta:
        model = models.Issue
        fields = ('id', 'description')

    def create(self, validated_data):
        """Create and return new user"""
        project = models.Project.objects.create_project(
            name=validated_data['description'],
            author=self.get_contributor(self.context['request'].user),
            issue=self.contex['request'].issue
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

class IssueSerializer(BaseSerializer):
    """Serializes Project model"""
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Issue
        fields = '__all__'
    

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

class ProjectSerializer(BaseSerializer):
    """Serializes Project model"""
    issues = IssueSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = ['id', 'url', 'name', 'issues']

    def create(self, validated_data):
        """Create and return new user"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
        )

        return project
