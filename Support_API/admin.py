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

admin.site.register(models.Project)
admin.site.register(models.Issue)
admin.site.register(models.Comment)
admin.site.register(models.ContributorProjet, ContributorProjetAdmin)
