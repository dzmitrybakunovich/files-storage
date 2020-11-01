import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    path = models.CharField(max_length=400, null=False, default=None)

    def create_path(self):
        self.path = os.path.join(settings.USERFILES_DIR, self.username)
        os.mkdir(self.path)
        return self.path

    def __str__(self):
        return self.username


class Folder(models.Model):
    folder_path = models.CharField(max_length=400, null=False, default=None)
    name = models.CharField(max_length=40, null=False, default=None)
    created = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField('api.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.folder_path


class LastOpenedToUser(models.Model):
    user = models.OneToOneField('api.CustomUser', on_delete=models.CASCADE)
    lastopened = models.DateTimeField(auto_now=True)
