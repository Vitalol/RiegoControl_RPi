"""
This file contais the classes and functions needed for riegocontrol protocol handling.
"""
import struct
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')

django.setup()
from sensors.models import Measure as dbMeaseure
from sensors.models import Sensor as dbSensor

RCPROTOLO_HEADER_SIZE = 4
RCPROTOLO_HEADER_RECEIVER_INDX = 0
RCPROTOLO_HEADER_SENDER_INDX = 1
RCPROTOLO_HEADER_MSG_PROTOCOL_INDX = 2
RCPROTOLO_HEADER_SIZE_INDX = 3

RCPROTOCOL_NONE                 = 0
RCPROTOCOL_MSG_SET_TIME         = 1
RCPROTOCOL_MSG_DEFAULT_RULE     = 2
RCPROTOCOL_MSG_SET_SCHEDULER    = 3
RCPROTOCOL_MSG_SEND_MEASURE     = 4
RCPROTOCOLMSG_MANUAL_ACTIVATION = 5
RCPROTOCOL_MSG_ACTUATION_RULE   = 6


class Measure:
    def __init__(self, value:float, type:int):
        self.value = value
        self.type = type

class Scheduler:

    def __init__(self, week_days:int, hour:int, minute:int):
        self.week_days = week_days
        self.hour = hour
        self.minute = minute


class RCProtocolHeader:

    def __init__(self, message) -> None:
        self.destination = message[RCPROTOLO_HEADER_RECEIVER_INDX]
        self.origin = message[RCPROTOLO_HEADER_SENDER_INDX]
        self.type = message[RCPROTOLO_HEADER_MSG_PROTOCOL_INDX]
        self.lenght = message[RCPROTOLO_HEADER_SIZE_INDX]
    
class RCProtocolSetHour:
    def __init__(self, header:RCProtocolHeader, time:int):
        self.header = header
        self.time = time

class RCProtocolSetScheduler:
    def __init__(self, header:RCProtocolHeader, actuator_id:int, scheduler:Scheduler):
        self.header = header
        self.actuator_id = actuator_id 
        self.scheduler = scheduler

class RCProtocolSendMeasure:

    def __init__(self, message, header:RCProtocolHeader):
        self.header = header
        self.message = message
        self.measures_num = self.message[RCPROTOLO_HEADER_SIZE]
        self.unpack_code = "<" + "fB"*self.measures_num

        measures_unpack = struct.unpack(self.unpack_code, self.message[RCPROTOLO_HEADER_SIZE+1:])
        
        self.measures = [(measures_unpack[i], measures_unpack[i + 1]) for i in range(0, len(measures_unpack), 2)]
    
    def get_measures_num(self) -> int:
        return self.measures_num
    
    def get_measures(self) -> list[Measure]:
        return self.measures



class RCProtocolManualActivation:
    def __init__(self, header:RCProtocolHeader, actuator_id:int, duration:int):
        self.header = header
        self.actuator_id = actuator_id
        self.duration = duration

def rc_protocol_handle_received_msg(message):
    """ Translate the protocol message

    Args:
        message (_type_): _description_
    """
    
    # First bytes are the header
    header = RCProtocolHeader(message=message)
    
    
    if (header.type == RCPROTOCOL_NONE):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_SET_TIME):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_DEFAULT_RULE):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_SET_SCHEDULER):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_SEND_MEASURE):
        
        received_measure =RCProtocolSendMeasure(
            message=message,
            header=header
        )
        
        sensor = dbSensor.objects.get(id=received_measure.header.origin)
        for measure in received_measure.get_measures():

            measure_db = dbMeaseure(sensor = sensor,
                                type = measure[1],
                                value =  measure[0])
            measure_db.save()

        pass
    elif (header.type == RCPROTOCOLMSG_MANUAL_ACTIVATION):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_ACTUATION_RULE) :
        #should not be received
        pass


# Send measure
cadena_bytes = '00 01 04 13 03 00 00 20 41 01 00 00 A0 41 02 00 00 F0 41 03'
bytestream = bytes.fromhex(cadena_bytes.replace(' ', ''))
print(bytestream)
# send_measure =RCP.RCProtocolSendMeasure(
#     message=bytestream,
#     header=RCP.RCProtocolHeader(bytestream)
# )
# atributos = vars(send_measure)
# for atributo, valor in atributos.items():
#     print(atributo, ":", valor)

rc_protocol_handle_received_msg(bytestream)