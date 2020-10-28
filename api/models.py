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
