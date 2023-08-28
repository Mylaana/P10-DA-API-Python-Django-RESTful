from django.db import models
from UserProfile_API.models import Contributor


class ProjectManager(models.Manager):
    """Database Project manager model"""
    def create_project(self, name, author):
        """Handles project creation"""

        if not author:
            raise ValueError("The Project must have an author")

        project = Project.objects.create(author=author, name=name)
        ContributorProjet.objects.create(project=project, contributors=author)

        return project

class IssueManager(models.Manager):
    """Database Issue manager model"""
    def create_issue(self, name, author, project, description, priority, issue_type, progression):
        """Handles Issue creation"""

        issue = Issue.objects.create(
            name=name, author=author, project=project, description=description,
            priority=priority, issue_type=issue_type, progression=progression)

        return issue


class CommentManager(models.Manager):
    """Database Project manager model"""
    def create_comment(self, issue, author, description):
        """Handles comment creation"""

        comment = Comment.objects.create(issue=issue, author=author, description=description)

        return comment


class Project(models.Model):
    """Database Project class model"""
    name = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(Contributor, through='ContributorProjet',
                                          related_name='projects_contributed')
    author = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True,
                               related_name='projects_authored')

    objects = ProjectManager()


class Issue(models.Model):
    """Database Issue model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
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

    objects = CommentManager()

class ContributorProjet(models.Model):
    """Database ptoject-contributors in between table"""
    contributors = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
