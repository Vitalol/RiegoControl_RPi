from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
import datetime
# Create your models here.
class Sensor(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    types = models.CharField(max_length = 255)
    change_pendig = models.BooleanField(default = False)
    
    @classmethod
    def get_default_pk(cls):
        sensor, created = cls.objects.get_or_create(
            name = "Default Sensor"
        )
        return sensor.pk


class Measure(models.Model):
    sensor = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, default= Sensor.get_default_pk
        )
    type = models.IntegerField(default = 0) # 0 Temperature 1 Humidity 2 Atmospheric Pressure
    value = models.FloatField(default = 0)
    date = models.DateTimeField(default = datetime.datetime.now)

class Actuator(models.Model):
    name = models.CharField(max_length = 255, unique = True)
    types = models.CharField(max_length = 255)
    change_pendig = models.BooleanField(default = False)

    @classmethod
    def get_default_pk(cls):
        sensor, created = cls.objects.get_or_create(
            name = "Default Actuator"
        )
        return sensor.pk
    
class Schedule(models.Model):
    actuator = models.ForeignKey(
        Actuator, on_delete=models.CASCADE, default= Actuator.get_default_pk
        )
    active = models.BooleanField(default = False)
    week_days = models.IntegerField(default = 0)
    hour = models.IntegerField(default = 0)
    minute = models.IntegerField(default = 0)


class Rules(models.Model):
    actuator = models.ForeignKey(
        Actuator, on_delete=models.CASCADE, default= Actuator.get_default_pk
        )
    active = models.BooleanField(default = False)
    type = models.IntegerField(default = 0)
    value = models.FloatField(default = 0)
    rule = models.IntegerField(default = 0) # 0 Larger or equal 1 Less
