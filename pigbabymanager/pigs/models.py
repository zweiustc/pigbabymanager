from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pigs(models.Model):
    uuid = models.CharField(max_length=36)
