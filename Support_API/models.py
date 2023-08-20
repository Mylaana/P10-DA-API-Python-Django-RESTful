from django.db import models
from UserProfile_API.models import Contributor


class ProjectManager(models.Manager):
    """Database Project manager model"""
    def create_project(self, name, author):
        """Handles project creation"""
        contribution = ContributorProjet()
        project = Project()

        contribution.contributors = author
        contribution.is_author = True
        contribution.project = project

        project.name = name
        project.contributors = author

        contribution.save()
        project.save()

        return project


class Project(models.Model):
    """Database Project class model"""
    name = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    contributors = models.ManyToManyField(Contributor, through='ContributorProjet',
                                          related_name='projects_contributed')
    author = models.ForeignKey(Contributor, on_delete=models.SET_NULL, null=True,
                               related_name='projects_authored')

    objects = ProjectManager()


class ContributorProjet(models.Model):
    """Database ptoject-contributors in between table"""
    contributors = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Issue(models.Model):
    """Database Issue model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
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
    type = models.IntegerField(choices=type_choices)

    progression_choices = (
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Finished'),
    )
    progression = models.IntegerField(choices=progression_choices)


class Comment(models.Model):
    """Database Comment model"""
    Issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=2048)
