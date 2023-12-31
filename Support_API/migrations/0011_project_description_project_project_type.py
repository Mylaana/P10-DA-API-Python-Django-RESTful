# Generated by Django 4.2.4 on 2023-08-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Support_API', '0010_alter_contributorprojet_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default=1, max_length=2048),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.IntegerField(choices=[(1, 'back-end'), (2, 'front-end'), (3, 'iOS'), (4, 'Android')], default=1),
            preserve_default=False,
        ),
    ]
