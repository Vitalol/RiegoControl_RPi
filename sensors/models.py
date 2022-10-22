from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime
# Create your models here.
class Sensor(models.Model):
    type = models.IntegerField(default = 1)
    name = models.CharField(max_length = 255)
    value = models.FloatField(default = 0)
    date = models.TimeField(default = datetime.datetime.now) 
