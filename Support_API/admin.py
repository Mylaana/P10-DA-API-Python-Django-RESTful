from django.contrib import admin
from Support_API import models

admin.site.register(models.Project)
admin.site.register(models.Issue)
admin.site.register(models.Comment)
