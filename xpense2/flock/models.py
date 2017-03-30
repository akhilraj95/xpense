from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    userId = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    def __str__(self):
        return self.userId
