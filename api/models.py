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
    folder_path = models.CharField(max_length=415, null=False, unique=True)
    name = models.CharField(max_length=40, null=False, default=None)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    owner = models.ForeignKey(
        'api.CustomUser',
        on_delete=models.CASCADE,
        related_name='folders',
    )

    def create_folder(self):
        self.folder_path = os.path.join(
            self.owner.path,
            self.name
        ) if not self.parent else os.path.join(
            self.parent.folder_path,
            self.name
        )
        try:
            os.mkdir(self.folder_path)
        except OSError:
            pass

    def save(self, *args, **kwargs):
        self.create_folder()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.folder_path
