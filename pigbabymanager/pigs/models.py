from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pig(models.Model):
    uuid = models.CharField(max_length=36)
    ear_tag = models.CharField(max_length=36)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    pig_type = models.CharField(max_length=36)
    location_id = models.CharField(max_length=100)
    manager_id = models.CharField(max_length=100)

    def __unicode__(self):
        return self.uuid
