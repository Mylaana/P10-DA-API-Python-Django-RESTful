# Generated by Django 4.2.4 on 2023-08-20 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile_API', '0004_userprofile_can_be_contacted_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='contact_me',
        ),
    ]
