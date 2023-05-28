import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')
django.setup()
from sensors.models import Sensor, Measure

import random
from datetime import timedelta, datetime
from enum import Enum

# class syntax

class MEASURE_TYPE(Enum):
    TEMPERATURE = 0
    HUMIDITY = 1
    ATM_PRESSION = 2

measure_ranges = {MEASURE_TYPE.TEMPERATURE.value:[20,30],
                  MEASURE_TYPE.HUMIDITY.value:[55,85],
                  MEASURE_TYPE.ATM_PRESSION.value:[1013,1042]}

def generate_weather_data(start_date, num_days, measure_type):
    weather_data = []
    current_date = start_date
    range_min = measure_ranges[measure_type][0]
    range_max = measure_ranges[measure_type][1]
    for _ in range(num_days):
        for _ in range(96):  # 96 períodos de 15 minutos en un día
            data = round(random.uniform(range_min, range_max), 1)  # Generar una temperatura aleatoria entre 20 y 30 grados Celsius
            weather_data.append((current_date, data))
            current_date += timedelta(minutes=15)

        current_date += timedelta(days=1)  # Pasar al siguiente día

    return weather_data

# Configuración de fechas
start_date = datetime.now() - timedelta(days=14)  # Fecha de inicio hace dos semanas
num_days = 14

# Generar sensores
sensor_temp = Sensor(name = "Temperature", types = "0,1,2")
sensor_humidity = Sensor(name = "Humidity", types = "1")
sensor_atm_pression = Sensor(name = "ATM Pression", types = "2")

sensors = [sensor_temp, sensor_humidity, sensor_atm_pression]

try:
    for sensor in sensors:
        sensor.save()
except:
    print("Sensors already generated")

for sensor in sensors:
    sensor_types = lista_enteros = [int(num) for num in sensor.types.split(",")]
    print(sensor_types)
    for measure_type in sensor_types:
        weather_data = generate_weather_data(start_date, num_days, measure_type)
        for data in weather_data:
            measure = Measure(
                sensor = sensor,
                type = measure_type,
                value = data[1],
                date = data[0]
            )
            measure.save()
    # Imprimir los resultados
    #for data in weather_data:
        #print(data)

