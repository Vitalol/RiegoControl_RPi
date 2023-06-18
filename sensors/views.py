from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sensors.models import Sensor
from sensors.models import Actuator

def sensors_conf(request, sensor_id):

    sensor = Sensor.objects.get(id=sensor_id)
    actuators = Actuator.objects.all()
    context = {
        'sensor': sensor,
        "actuators": actuators
    }
    template = loader.get_template("sensor_config.html")
    print(f'{sensor.name}')
    return HttpResponse(template.render(context, request))

def sensors_conf_rule(request, sensor_id):
    tipo = request.POST.get('tipo')
    condicion = request.POST.get('condicion')
    valor = request.POST.get('valor',0)
    actuator = Actuator.objects.get(id=request.POST.get('actuator'))
    print(f"{tipo} {condicion} {valor} {sensor_id} {actuator.name}")
    return HttpResponse(f"{tipo} {condicion} {valor} {sensor_id} {actuator.name}")

def sensors_conf_schedule(request, sensor_id):


    dias_lista =request.POST.getlist('dias')
    dias = (sum(int(dia) for dia in dias_lista))
    dias_binary = bin(dias)
    hora = request.POST.get('hora',0)
    actuator = Actuator.objects.get(id=request.POST.get('actuator'))
    print(f"{(dias_binary)} {hora} {actuator.name}")
    return HttpResponse(f"{(dias_binary)} {hora} {actuator.name}")