from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sensors.models import Sensor
from sensors.models import Actuator
from sensors.models import Rules
from sensors.models import Schedule

def delete_rule(actuator):
    instance = Rules.objects.filter(actuator = actuator)
    if instance.exists():
        instance.delete()

def delete_schdl(actuator):
    instance = Schedule.objects.filter(actuator = actuator)
    if instance.exists():
        instance.delete()

def delete_conf(actuator):
    delete_rule(actuator)
    delete_schdl(actuator)

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
    # take parameters
    tipo = request.POST.get('tipo')
    condicion = request.POST.get('condicion')
    valor = request.POST.get('valor',0)
    actuator = Actuator.objects.get(id=request.POST.get('actuator'))
    print(f"{tipo} {condicion} {valor} {sensor_id} {actuator.name}")
    
    # Delete previous rule/schedule
    delete_conf(actuator)

    # make model from parameteres
    rule = Rules(actuator = actuator,
                 active = True,
                type = tipo,
                value = valor,
                rule = condicion)
    
    # Save it
    rule.save()
    # mark actuator as change pending
    actuator.change_pendig = 1
    actuator.save()
    return HttpResponse(f"{tipo} {condicion} {valor} {sensor_id} {actuator.name}")

def sensors_conf_schedule(request, sensor_id):
    # take parameters
    dias_lista =request.POST.getlist('dias')
    dias = (sum(int(dia) for dia in dias_lista))
    dias_binary = bin(dias)
    hora = request.POST.get('hora',0)
    actuator = Actuator.objects.get(id=request.POST.get('actuator'))
    print(f"{(dias_binary)} {hora} {actuator.name}")
    # hora (str) to hours and minutes
    hours, minutes = map(int, hora.split(":"))
    print("Hours:", hours)
    print("Minutes:", minutes)
    # Delete previous rule/schedule
    delete_conf(actuator)

    # make model from parameteres
    schedule = Schedule(
        actuator = actuator,
        active = True,
        week_days = dias,
        hour = hours,
        minute = minutes
    )
    schedule.save()

    # mark actuator as change pending
    actuator.change_pendig = 1
    actuator.save()
    return HttpResponse(f"{(dias_binary)} {hora} {actuator.name}")
