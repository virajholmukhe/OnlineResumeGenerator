# Generated by Django 4.0.5 on 2022-07-01 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='academic_project',
            old_name='project_title',
            new_name='project_title2',
        ),
    ]
