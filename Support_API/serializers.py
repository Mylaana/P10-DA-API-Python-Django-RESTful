from rest_framework import serializers
from rest_framework.fields import empty
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
    serializer_url = ''
    excluded_fields = []
    url_name_project = 'project'
    url_name_issue = 'issue'
    url_name_comment = 'comment'

    def get_parent_url(self, obj):
        return ""

    def get_url(self, obj):
        request = self.context.get('request', None)
        if not request:
            return
        self.parent_url = self.get_parent_url(obj)

        request_url = request.build_absolute_uri("/")
        return request_url + self.parent_url + self.serializer_url + str(obj.id)

class CommentSerializer(BaseSerializer):
    """Serializes Comment model"""
    url = serializers.SerializerMethodField()
    serializer_url = 'comment/'

    class Meta:
        model = models.Comment
        fields = '__all__'

    def create(self, validated_data):
        """Create and return new comment"""
        comment = models.Comment.objects.create_comment(
            description=validated_data['description'],
            author=get_contributor(self.context['request'].user),
            issue=validated_data['issue']
        )

        return comment

    def get_project_id(self, obj):
        return obj.issue.project.id

    def get_parent_url(self, obj):
        project_url = str(self.url_name_project) + "/"  + str(obj.issue.project.id) + "/" + str(self.url_name_issue) + "/"  + str(obj.issue.id) + "/"
        return str(project_url)

class IssueSerializer(BaseSerializer):
    """Serializes Issue model"""
    class Meta:
        model = models.Issue
        fields = '__all__'
    comments = CommentSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    serializer_url = 'issue/'



    def create(self, validated_data):
        """Create and return new Issue"""
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

    def get_project_id(self, obj):
        return obj.project.id

    def get_parent_url(self, obj):
        project_url = str(self.url_name_project) + "/"  + str(obj.project.id) + "/"
        return str(project_url)

class ProjectSerializer(BaseSerializer):
    """Serializes Project model"""
    issues = IssueSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    parent_url = ''
    serializer_url = 'project/'

    class Meta:
        model = models.Project
        fields = '__all__'

    def create(self, validated_data):
        """Create and return new Project"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
        )

        return project
