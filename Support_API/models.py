import uuid
from django.db import models
from UserProfile_API.models import Contributor


class ProjectManager(models.Manager):
    """Database Project manager model"""
    def create_project(self, name, author, description, project_type):
        """Handles project creation"""

        if not author:
            raise ValueError("The Project must have an author")

        project = Project.objects.create(author=author, name=name, description=description, project_type=project_type)
        ContributorProjet.objects.create(project=project, contributors=author)

        return project

class IssueManager(models.Manager):
    """Database Issue manager model"""
    def create_issue(self, name, author, project, description, priority, issue_type, progression, assigned_to):
        """Handles Issue creation"""
        print(assigned_to)
        issue = Issue.objects.create(
            name=name, author=author, project=project, description=description,
            priority=priority, issue_type=issue_type, progression=progression, assigned_to=assigned_to)

        return issue


class CommentManager(models.Manager):
    """Database Comment manager model"""
    def create_comment(self, issue, author, description):
        """Handles comment creation"""

        comment = Comment.objects.create(issue=issue, author=author, description=description)

        return comment

class ContributionManager(models.Manager):
    """Database Contribution-project manager model"""

    def create_contribution(self, contributors, project):
        """Handles Contribution creation"""

        if not project:
            raise ValueError("Please select a project")

        if ContributorProjet.objects.filter(contributors=contributors, project=project).exists():
            raise ValueError("You are already contributing to this project")

        contribution = ContributorProjet.objects.create(contributors=contributors, project=project)

        return contribution

class Project(models.Model):
    """Database Project class model"""
    name = models.CharField(max_length=255, unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(Contributor, through='ContributorProjet',
                                          related_name='projects_contributed')
    author = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True,
                               related_name='projects_authored')

    description = models.TextField(max_length=2048)
    type_choices = (
        (1, 'back-end'),
        (2, 'front-end'),
        (3, 'iOS'),
        (4, 'Android'),
    )
    project_type = models.IntegerField(choices=type_choices)

    objects = ProjectManager()


class Issue(models.Model):
    """Database Issue model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='assigned_to', null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=2048)

    priority_choices = (
        (1, 'LOW'),
        (2, 'MEDIUM'),
        (3, 'HIGH'),
    )
    priority = models.IntegerField(choices=priority_choices)

    type_choices = (
        (1, 'BUG'),
        (2, 'FEATURE'),
        (3, 'TASK'),
    )
    issue_type = models.IntegerField(choices=type_choices)

    progression_choices = (
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Finished'),
    )
    progression = models.IntegerField(choices=progression_choices)

    objects = IssueManager()

class Comment(models.Model):
    """Database Comment model"""
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=2048)
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False,
        unique = True)

    objects = CommentManager()


class ContributorProjet(models.Model):
    """Database project-contributors many-to-many in between table"""
    contributors = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    objects = ContributionManager()
    class Meta:
        unique_together = ('contributors', 'project')

    def __str__(self):
        return f"Contribution id: {self.id}, Username: {self.contributors.user_profile.username}, project id: {self.project.id}"