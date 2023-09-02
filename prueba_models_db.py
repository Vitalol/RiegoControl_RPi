import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')

django.setup()
from sensors.models import Sensor
from sensors.models import Measure

Measure.objects.get(id=6721).delete()
Measure.objects.get(id=6722).delete()
Measure.objects.get(id=6723).delete()