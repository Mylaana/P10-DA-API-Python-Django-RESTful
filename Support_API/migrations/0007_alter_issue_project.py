# Generated by Django 4.2.4 on 2023-08-24 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Support_API', '0006_rename_type_issue_issue_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='Support_API.project'),
        ),
    ]
