from django.contrib import admin
from Support_API import models


class ContributorProjetAdmin(admin.ModelAdmin):
    list_display = ("contribution_id", "project_id", "user_id", "user_name", "project_name")

    def project_id(self, obj):
        return obj.project.id

    def contribution_id(self, obj):
        return obj.id

    def user_id(self,obj):
        return obj.contributors.user_profile.id

    def user_name(self,obj):
        return obj.contributors.user_profile.username
    
    def project_name(self,obj):
        return obj.project.name

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author_name", "project_type")

    def author_name(self,obj):
        return obj.author.user_profile.username

class IssueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author_name", "project_id", "project_name")

    def author_name(self,obj):
        return obj.author.user_profile.username
    
    def project_id(self,obj):
        return obj.project.id

    def project_name(self,obj):
        return obj.project.name

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author_name", "project_id", "project_name", "issue_id", "issue_name", "description")

    def author_name(self,obj):
        return obj.author.user_profile.username
    
    def project_id(self,obj):
        return obj.issue.project.id

    def project_name(self,obj):
        return obj.issue.project.name

    def issue_id(self,obj):
        return obj.issue.id

    def issue_name(self,obj):
        return obj.issue.name

admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.ContributorProjet, ContributorProjetAdmin)
