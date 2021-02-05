# Generated by Django 3.1.2 on 2020-11-01 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_folder_lastopenedtouser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='lastupdated',
        ),
        migrations.AddField(
            model_name='folder',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='api.folder'),
        ),
        migrations.DeleteModel(
            name='LastOpenedToUser',
        ),
    ]
