from django.db import models
from django.contrib.postgres.fields import HStoreField
from jsonfield import JSONField


# Create your models here.
class Object(models.Model):
    object_id = models.IntegerField()
    object_img = models.CharField(max_length=900000)
    # features = HStoreField()
    features = JSONField()