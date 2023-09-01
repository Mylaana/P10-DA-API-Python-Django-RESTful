from django.contrib import admin
from UserProfile_API import models

class ContributorAdmin(admin.ModelAdmin):
    list_display = ("contributor_id", "contributor_name")

    def contributor_id(self,obj):
        return obj.user_profile.id

    def contributor_name(self,obj):
        return obj.user_profile.username

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_of_birth", "can_be_contacted", "can_data_be_shared", "is_active", "is_admin", "is_staff",)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Contributor, ContributorAdmin)
