# Generated by Django 3.1.2 on 2021-05-27 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_foldershare'),
    ]

    operations = [
        migrations.RenameField(
            model_name='foldershare',
            old_name='Folder',
            new_name='folder',
        ),
    ]