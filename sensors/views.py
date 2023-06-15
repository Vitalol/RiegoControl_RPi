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

def sensors_conf_rule(request, sensor_id):
    tipo = request.POST.get('tipo')
    condicion = request.POST.get('condicion')
    valor = request.POST.get('valor')
    print(f"{tipo} {condicion} {valor} {sensor_id}")
    return HttpResponse(f"{tipo} {condicion} {valor} {sensor_id}")

def sensors_conf_schedule(request, sensor_id):


    dias_lista =request.POST.getlist('dias')
    dias = (sum(int(dia) for dia in dias_lista))
    dias_binary = bin(dias)
    hora = request.POST.get('hora')
    print(f"{(dias_binary)} {hora}")
    return HttpResponse(f"{(dias_binary)} {hora}")