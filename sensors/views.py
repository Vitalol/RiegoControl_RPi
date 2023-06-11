from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sensors.models import Sensor

def sensors_conf(request, sensor_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        return HttpResponse(f"{nombre} {direccion}")
    

    sensor = Sensor.objects.get(id=sensor_id)
    context = {
        'sensor': sensor,
    }
    template = loader.get_template("sensor_config.html")
    print(f'{sensor.name}')
    return HttpResponse(template.render(context, request))
