import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')
django.setup()
from sensors.models import Actuator

Actuator.objects.all().delete()

actuator1 = Actuator(name = "Test Actuator 1", types = '1')
actuator2 = Actuator(name = "Test Actuator 2", types = '1, 2')
actuator3 = Actuator(name = "Test Actuator 3", types = '3')

actuator1.save()
actuator2.save()
actuator3.save()

