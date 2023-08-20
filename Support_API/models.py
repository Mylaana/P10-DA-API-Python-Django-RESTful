from django.db import models
from UserProfile_API.models import Contributor

class Project(models.Model):
    """Database Project class model"""
    created_time = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2048)
    contributors = []

    priority_choices = (
        (1, 'LOW'),
        (2, 'MEDIUM'),
        (3, 'HIGH'),
    )
    priority = models.IntegerField(max_length=1, choices=priority_choices)

    type_choices = (
        (1, 'BUG'),
        (2, 'FEATURE'),
        (3, 'TASK'),
    )
    type = models.IntegerField(max_length=1, choices=type_choices)

    progression_choices = (
        (1, 'To Do'),
        (2, 'In Progress'),
        (3, 'Finished'),
    )
    progression = models.IntegerField(max_length=1, choices=progression_choices)

class Comment(models.Model):
    Issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=2048)
