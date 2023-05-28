from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime
# Create your models here.
class Sensor(models.Model):
    type = models.IntegerField(default = 1)
    name = models.CharField(max_length = 255)
    change_pendig = models.BooleanField(default = False)
    schedule_active = models.BooleanField(default = False)


class Measure(models.Model):
    sensor = models.ForeignKey(Sensor)
    type = models.IntegerField(default = 1)
    value = models.FloatField(default = 0)
    date = models.DateTimeField(default = datetime.datetime.now)


class schedule(models.Model):
    sensor = models.ForeignKey(Sensor)
    month_days = models.IntegerField(default = 0)
    week_days = models.IntegerField(default = 0)
    hour = models.IntegerField(default = 0)
    minute = models.IntegerField(default = 0)
    active = models.BooleanField(default = False)
