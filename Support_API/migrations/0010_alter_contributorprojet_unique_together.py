# Generated by Django 4.2.4 on 2023-08-30 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile_API', '0007_alter_userprofile_can_be_contacted_and_more'),
        ('Support_API', '0009_alter_comment_issue'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributorprojet',
            unique_together={('contributors', 'project')},
        ),
    ]
