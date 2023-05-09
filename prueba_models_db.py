import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')

django.setup()
from sensors.models import Sensor

print(Sensor.objects.all().values())
lectura = Sensor(name = "Montaña", value =24)
lectura.save()

montaña = Sensor.objects.filter(name = "Montaña")
print(montaña.values())
