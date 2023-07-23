from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sensors.models import Sensor
from sensors.models import Actuator
from sensors.models import Rules
from sensors.models import Schedule
import sensors.rc_protocol as RCP
import socket

# Definir la dirección IP y el puerto del servidor
IP_SERVIDOR = "127.0.0.1"  # Dirección IP del servidor
PUERTO_SERVIDOR = 54321    # Puerto del servidor

def send_socket(msg:bytearray):
    # Crear un socket TCP/IP
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conectar el cliente al servidor
    cliente_socket.connect((IP_SERVIDOR, PUERTO_SERVIDOR))

    # Enviar datos al servidor
    
    cliente_socket.sendall(msg)

    # Esperar la respuesta del servidor
    datos_recibidos = cliente_socket.recv(1024)

    # Decodificar y mostrar la respuesta del servidor
    print("Respuesta del servidor:", datos_recibidos.decode())

    # Cerrar la conexión con el servidor
    cliente_socket.close()

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
    send_socket("conf_rule")
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
    head = RCP.RCProtocolHeader(destination=1,
                        origin=RCP.RCPROTOLO_SINK_INDX,
                        type=RCP.RCPROTOCOL_MSG_SET_SCHEDULER,
                        length=RCP.RCPROTOCOL_SET_SCHEDULER_SIZE)
    
    schedule = RCP.Scheduler(week_days= dias,
                         hour= hours,
                         minute=minutes)
    
    set_scheduler = RCP.RCProtocolSetScheduler(header=head,
                                           scheduler=schedule,
                                           actuator_id=2)
    send_socket(set_scheduler.packed)

    return HttpResponse(f"{(dias_binary)} {hora} {actuator.name}")
