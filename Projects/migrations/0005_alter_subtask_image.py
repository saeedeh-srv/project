# Generated by Django 5.1.1 on 2024-10-09 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0004_remove_subtask_task_subtask_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtask',
            name='image',
            field=models.ImageField(default='projects/default/project_d.png', upload_to='projects/subtask/'),
        ),
    ]
