# Generated by Django 4.2.4 on 2023-08-30 16:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Support_API', '0011_project_description_project_project_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
