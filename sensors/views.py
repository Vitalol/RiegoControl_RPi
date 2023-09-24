from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from sensors.models import Sensor
from sensors.models import Measure
from sensors.models import Actuator
from sensors.models import Rules
from sensors.models import Schedule
import sensors.rc_protocol as RCP
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import socket
import datetime
# Definir la dirección IP y el puerto del servidor
IP_SERVIDOR = "127.0.0.1"  # Dirección IP del servidor
PUERTO_SERVIDOR = 54321    # Puerto del servidor

from io import BytesIO
import base64

def tipo_medida(indx):
    
    tipo_medida = { 0: 'Temperatura', 1: 'Humedad', 2: 'Presión atmosferica'}
    return tipo_medida[indx]

def sensor_graph(request, sensor_id):
    # Datos para la gráfica
    # Obtengo sensor
    sensor = Sensor.objects.get(id=sensor_id)
    
    # Obtengo lista de medidas del sensor
    # Cadena de texto con números separados por comas

    measure_type_list = [int(subcadena) for subcadena in (sensor.types).split(",")]
    print(measure_type_list)
    graph_list = []
    for measure_type in measure_type_list:
        plt.clf()
        #Obtengo medidas para cadda tipo de medida
        measures = Measure.objects.filter(sensor=sensor, type = measure_type)
        measures_values_data = [(measure.date, measure.value)  for measure in measures]
        measures_values_data_ordenada = sorted(measures_values_data, key=lambda tupla: tupla[0])
    

        fecha_fin = measures_values_data_ordenada[-10:][0][0]
        print(fecha_fin)
        fecha_inicio = fecha_fin -  datetime.timedelta(days=1)

        tuplas_en_rango = [(fecha, valor) for fecha, valor in measures_values_data if fecha_inicio <= fecha <= fecha_fin]

        x, y = zip(*tuplas_en_rango)
        # Crear la gráfica
        plt.plot(x, y)
        plt.xlabel('Fecha')
        plt.ylabel('Valor')
        plt.title(f'Medida de {tipo_medida(measure_type)}')

        # Guardar la gráfica en un objeto BytesIO en lugar de un archivo
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = buffer.getvalue()
        buffer.close()

        # Codificar la imagen en base64 para mostrar en una etiqueta de imagen HTML
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        graph_list.append(image_base64)
    print(len(graph_list))
    context = {'image_base64': graph_list, 'sensor_name': sensor.name}
    return render(request, 'grafica.html', context)


def send_socket(msg: bytearray):
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
    instance = Rules.objects.filter(actuator=actuator)
    if instance.exists():
        instance.delete()


def delete_schdl(actuator):
    instance = Schedule.objects.filter(actuator=actuator)
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
    return HttpResponse(template.render(context, request))

def actuator_conf(request, actuator_id):

    sensors = Sensor.objects.all()
    actuator = Actuator.objects.get(id=actuator_id)
    context = {
        'sensors': sensors,
        "actuator": actuator
    }
    template = loader.get_template("actuator_config.html")
    return HttpResponse(template.render(context, request))

def conf_rule(request, actuator_id):

    # take parameters
    tipo = request.POST.get('tipo')
    condicion = request.POST.get('condicion')
    valor = request.POST.get('valor', 0)
    actuator = Actuator.objects.get(id=actuator_id)
    print(f"{tipo} {condicion} {valor} {actuator_id} {actuator.name}")

    # Delete previous rule/schedule
    delete_conf(actuator)

    # make model from parameteres
    rule = Rules(actuator=actuator,
                 active=True,
                 type=tipo,
                 value=valor,
                 rule=condicion)

    # Save it
    rule.save()
    # mark actuator as change pending
    actuator.change_pendig = 1
    actuator.save()

    head = RCP.RCProtocolHeader(destination=rule.actuator.lora_id,
                                origin=RCP.RCPROTOLO_SINK_INDX,
                                type=RCP.RCPROTOCOL_MSG_ACTUATION_RULE,
                                length=RCP.RCPROTOCOL_SET_RULE_SIZE)

    rule = RCP.Rule(rule=int(rule.rule),
                    value=float(rule.value),
                    type=int(rule.rule))

    set_rule = RCP.RCProtocolSetRule(header=head,
                                     rule=rule,
                                     actuator_id=2)
    send_socket(set_rule.packed)

def actuator_conf_rule(request, actuator_id):

    
    conf_rule(request, actuator_id)

    return HttpResponse("Hola")

def actuator_conf_schedule(request, actuator_id):


    return HttpResponse("Hola")

def sensors_conf_schedule(request, sensor_id):
    # take parameters
    dias_lista = request.POST.getlist('dias')
    dias = (sum(int(dia) for dia in dias_lista))
    dias_binary = bin(dias)
    hora = request.POST.get('hora', 0)
    actuator = Actuator.objects.get(id=request.POST.get('actuator'))
    duration = request.POST.get('duration', 0)
    print(f"{(dias_binary)} {hora} {actuator.name}")
    # hora (str) to hours and minutes
    hours, minutes = map(int, hora.split(":"))
    print("Hours:", hours)
    print("Minutes:", minutes)
    # Delete previous rule/schedule
    delete_conf(actuator)

    # make model from parameteres
    schedule = Schedule(
        actuator=actuator,
        active=True,
        week_days=dias,
        hour=hours,
        minute=minutes,
        duration=duration
    )
    schedule.save()

    # mark actuator as change pending
    actuator.change_pendig = 1
    actuator.save()
    head = RCP.RCProtocolHeader(destination=schedule.actuator.lora_id,
                                origin=RCP.RCPROTOLO_SINK_INDX,
                                type=RCP.RCPROTOCOL_MSG_SET_SCHEDULER,
                                length=RCP.RCPROTOCOL_SET_SCHEDULER_SIZE)

    schedule = RCP.Scheduler(week_days=schedule.week_days,
                             hour=schedule.hour,
                             minute=schedule.minute,
                             duration=int(duration))

    set_scheduler = RCP.RCProtocolSetScheduler(header=head,
                                               scheduler=schedule,
                                               actuator_id=2)
    send_socket(set_scheduler.packed)

    return HttpResponse(f"{(dias_binary)} {hora} {actuator.name}")


def actuator_conf_manual(request, actuator_id):

    return HttpResponse(f"Manual")