# Generated by Django 4.2.4 on 2023-08-31 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Support_API', '0013_remove_comment_id_comment_comment_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment_uuid',
            new_name='id',
        ),
    ]
