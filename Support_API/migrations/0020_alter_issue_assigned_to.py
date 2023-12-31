# Generated by Django 4.2.4 on 2023-09-05 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile_API', '0007_alter_userprofile_can_be_contacted_and_more'),
        ('Support_API', '0019_alter_issue_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='assigned_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to='UserProfile_API.contributor'),
        ),
    ]
