from rest_framework import serializers
from rest_framework.fields import empty
from Support_API import models
from UserProfile_API.models import Contributor

SERIALIZER_DEBUG = True

def get_contributor(user_id):
    """
    check if user is already a contributor on any project,
    adds them in contributor list if not

    returns a contributor id
    """

    contributor = Contributor.objects.filter(user_profile=user_id).first()
    if contributor is None:
        contributor = Contributor.objects.create(user_profile=user_id)

    return contributor

def get_contributor_name(contributor_id):
    """
    return contributor name from contributor id
    """
    contributor = Contributor.objects.filter(user_profile=contributor_id).first()
    if not contributor:
        return
    return contributor.user_profile.username

def get_contributors_name_list(contributors):
    contributor_names = []

    for contributor in contributors.all():
        contributor_name = get_contributor_name(contributor.user_profile_id)
        if contributor_name:
            contributor_names.append(contributor_name)

    return contributor_names

class BaseSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    url_new_item = serializers.SerializerMethodField()
    serializer_url = ''
    excluded_fields = []
    url_name_project = 'project'
    url_name_issue = 'issue'
    url_name_comment = 'comment'
    author_name = serializers.SerializerMethodField()

    def get_parent_url(self, obj):
        return ''

    def get_author_name(self, obj):
        return get_contributor_name(obj.author)

    def get_url(self, obj):
        request = self.context.get('request', None)
        if not request:
            return
        self.parent_url = self.get_parent_url(obj)

        request_url = request.build_absolute_uri("/")
        return request_url + self.parent_url + self.serializer_url + str(obj.id)

    def get_url_new_item(self, obj):
        request = self.context.get('request', None)
        if not request:
            return
        self.parent_url = self.get_parent_url(obj)

        request_url = request.build_absolute_uri("/")
        return request_url + self.parent_url + self.serializer_url 


class CommentSerializer(BaseSerializer):
    """Serializes Comment model"""
    url = serializers.SerializerMethodField()
    serializer_url = 'comment/'

    class Meta:
        model = models.Comment
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url', 'created_time', 'author_name', 'description']


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
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url', 'url_new_item', 'created_time', 'name', 'author_name','priority', 'issue_type', 'progression', 'comments']

    comments = CommentSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    serializer_url = 'issue/'

    priority = serializers.CharField(source='get_priority_display', read_only=True)
    issue_type = serializers.CharField(source='get_issue_type_display', read_only=True)
    progression = serializers.CharField(source='get_progression_display', read_only=True)


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
    contributors_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    parent_url = ''
    serializer_url = 'project/'

    class Meta:
        model = models.Project
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url','url_new_item', 'created_time', 'name', 'author_name', 'contributors_name', 'issues']


    def create(self, validated_data):
        """Create and return new Project"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
        )
        return project

    def get_contributors_name(self, obj):
        return get_contributors_name_list(obj.contributors.all())


class ContributionSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    class Meta:
        model = models.ContributorProjet
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url', 'project']


    def create(self, validated_data):
        """Create and return new user"""
        user = models.ContributorProjet.objects.create(
            project=validated_data['project'],
            contributors=get_contributor(self.context['request'].user),
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
    """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
    """