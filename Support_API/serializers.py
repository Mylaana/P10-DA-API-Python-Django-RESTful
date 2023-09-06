from rest_framework import serializers
from rest_framework.fields import empty
from Support_API import models
from UserProfile_API.models import Contributor

SERIALIZER_DEBUG = False

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

    def get_url_new_child(self, obj):
        request = self.context.get('request', None)
        if not request:
            return
        self.parent_url = self.get_parent_url(obj)

        request_url = request.build_absolute_uri("/")
        if isinstance(obj, models.Project):
            child_url = "/issue"
        elif isinstance(obj, models.Issue):
            child_url = "/comment"
        return request_url + self.parent_url + self.serializer_url + str(obj.id) + child_url

    def get_parent_id_from_url(self, request):
        return request.build_absolute_uri().split("/")[-3]

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
            issue=models.Issue.objects.get(id=self.get_parent_id_from_url(self.context['request']))
        )
        return comment

    def get_project_id(self, obj):
        return obj.issue.project.id

    def get_parent_url(self, obj):
        project_url = str(self.url_name_project) + "/"  + str(obj.issue.project.id) + "/" + str(self.url_name_issue) + "/"  + str(obj.issue.id) + "/"
        return str(project_url)

class IssueSerializer(BaseSerializer):
    """Serializes Issue model"""
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        project_id = 0
        for key, value in self.context.items():
            if key == 'project_id':
                project_id = int(value)
                break

        choice_list = self.get_assign_to_list(project_id)
        if not choice_list is None:
            self.fields['assign_issue_to'].choices = choice_list

    def get_assign_to_list(self, project_id):
        """returns a list of contributor to assign issue to as a list of tuples"""
        project = models.Project.objects.filter(id=project_id).first()
        if project is None:
            return None
        choice_list = [(0, None)]
        for contributor in project.contributors.all():
            choice_list.append((contributor.user_profile.id, contributor.user_profile.username))

        return choice_list

    class Meta:
        model = models.Issue
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url', 'add_new_comment', 'created_time', 'name', 'author_name','priority',
                      'priority_description', 'issue_type', 'issue_type_description', 'progression', 
                      'progression_description', 'assigned_to', 'assigned_to_name', 'assign_issue_to', 'description', 'comments']

        extra_kwargs = {
            'progression': {'write_only': True},
            'issue_type': {'write_only': True},
            'priority': {'write_only': True},
            'assigned_to': {'read_only': True},

        }

    comments = CommentSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()
    serializer_url = 'issue/'
    add_new_comment = serializers.SerializerMethodField()

    priority_description = serializers.CharField(source='get_priority_display', read_only=True)
    issue_type_description = serializers.CharField(source='get_issue_type_display', read_only=True)
    progression_description = serializers.CharField(source='get_progression_display', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()

    assign_issue_to = serializers.ChoiceField(choices=[], required=False)


    def create(self, validated_data):
        """Create and return new Issue"""

        if models.Contributor.objects.filter(user_profile_id=validated_data['assign_issue_to']).exists():
            contributor = models.Contributor.objects.get(user_profile_id=validated_data['assign_issue_to'])
        else:
            contributor = None
        print(contributor)
        issue = models.Issue.objects.create_issue(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
            project=models.Project.objects.get(id=self.get_parent_id_from_url(self.context['request'])),
            description=validated_data['description'],
            priority=validated_data['priority'],
            issue_type=validated_data['issue_type'],
            progression=validated_data['progression'],
            assigned_to=contributor
        )
        return issue

    def update(self, instance, validated_data):
        if 'assign_issue_to' in validated_data:
            assign_issue_to = validated_data.pop('assign_issue_to')
            if assign_issue_to:
                # Vérifiez si l'assigné existe en tant que Contributor
                if models.Contributor.objects.filter(user_profile_id=assign_issue_to).exists():
                    contributor = models.Contributor.objects.get(user_profile_id=assign_issue_to)
                else:
                    contributor = None
            else:
                contributor = None
            instance.assigned_to = contributor

        # Mettez à jour les autres champs de l'instance en fonction des données validées
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.issue_type = validated_data.get('issue_type', instance.issue_type)
        instance.progression = validated_data.get('progression', instance.progression)

        # Enregistrez les modifications de l'instance Issue
        instance.save()
        return instance

    def get_add_new_comment(self, obj):
        return self.get_url_new_child(obj)

    def get_project_id(self, obj):
        return obj.project.id

    def get_parent_url(self, obj):
        project_url = str(self.url_name_project) + "/"  + str(obj.project.id) + "/"
        return str(project_url)

    def get_assigned_to_name(self, obj):
        if obj.assigned_to is None:
            return ''
        return obj.assigned_to.user_profile.username

class ProjectSerializer(BaseSerializer):
    """Serializes Project model"""
    issues = IssueSerializer(many=True, read_only=True)
    contributors_name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    add_new_issue = serializers.SerializerMethodField()
    parent_url = ''
    serializer_url = 'project/'
    project_type_description = serializers.CharField(source='get_project_type_display', read_only=True)


    class Meta:
        model = models.Project

        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['url','add_new_issue', 'created_time', 'name',
                      'author_name', 'project_type', 'project_type_description',
                      'contributors_name', 'description', 'issues']

        extra_kwargs = {
            'project_type': {'write_only': True},
        }

    def create(self, validated_data):
        """Create and return new Project"""
        project = models.Project.objects.create_project(
            name=validated_data['name'],
            author=get_contributor(self.context['request'].user),
            description=validated_data['description'],
            project_type=validated_data['project_type'],
        )
        return project

    def get_contributors_name(self, obj):
        return get_contributors_name_list(obj.contributors.all())

    def get_add_new_issue(self, obj):
        return self.get_url_new_child(obj)

class ContributionSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    def get_project_name_list():
        """returns a list of tuple with [(id,project name),..]"""
        project_list = []
        for project in models.Project.objects.all():
            project_list.append((project.id, f"projet {project.id} : {project.name}"))

        return project_list

    contribute_to = serializers.ChoiceField(choices=get_project_name_list(), required=False)

    class Meta:
        model = models.ContributorProjet
        if SERIALIZER_DEBUG:
            fields = '__all__'
        else:
            fields = ['contribute_to']


    def create(self, validated_data):
        """Create and return new user"""
        try:
            contribution = models.ContributorProjet.objects.create_contribution(
                project=models.Project.objects.get(id=validated_data['contribute_to']),
                contributors=get_contributor(self.context['request'].user))
            return contribution

        except Exception as excep:
            error = {'message': ",".join(excep.args) if len(excep.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)
