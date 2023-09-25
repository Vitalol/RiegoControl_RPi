"""
This file contais the classes and functions needed for riegocontrol protocol handling.
"""
import struct
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')

django.setup()
from sensors.models import Measure as dbMeaseure
from sensors.models import Sensor as dbSensor

RCPROTOLO_SINK_INDX = 0

RCPROTOLO_HEADER_SIZE = 4
RCPROTOLO_HEADER_RECEIVER_INDX = 0
RCPROTOLO_HEADER_SENDER_INDX = 1
RCPROTOLO_HEADER_MSG_PROTOCOL_INDX = 2
RCPROTOLO_HEADER_SIZE_INDX = 3

RCPROTOCOL_NONE                     = 0
RCPROTOCOL_MSG_SET_TIME             = 1
RCPROTOCOL_MSG_DEFAULT_RULE         = 2
RCPROTOCOL_MSG_SET_SCHEDULER        = 3
RCPROTOCOL_MSG_SEND_MEASURE         = 4
RCPROTOCOL_MSG_MANUAL_ACTIVATION    = 5
RCPROTOCOL_MSG_ACTUATION_RULE       = 6



RCPROTOCOL_SET_SCHEDULER_SIZE       = 8
RCPROTOCOL_SET_RULE_SIZE            = 10
RCPROTOCOL_SET_TIME_SIZE            = 4
RCPROTOCOL_MANUAL_ACTIVATION_SIZE   = 6

class Measure:
    def __init__(self, value:float, type:int):
        self.value = value
        self.type = type

class Scheduler:

    def __init__(self, week_days:int, hour:int, minute:int, duration:int):
        self.month_days = 0
        self.week_days = week_days
        self.hour = hour
        self.minute = minute
        self.duration = duration
        format = "<IBBBI"
        self.packed = struct.pack(format, self.month_days, self.week_days, self.hour, self.minute, self.duration)

class Rule:

    def __init__(self, type:int, value:float, rule:int):
        self.type = type
        self.value = value
        self.rule = rule
        format = "<BfB"
        self.packed = struct.pack(format, self.type, self.value, self.rule)

class RCProtocolHeader:

    def __init__(self, message=0, destination=0, origin=0, type=0, length=0) -> None:
        if(message):
            self.destination = message[RCPROTOLO_HEADER_RECEIVER_INDX]
            self.origin = message[RCPROTOLO_HEADER_SENDER_INDX]
            self.type = message[RCPROTOLO_HEADER_MSG_PROTOCOL_INDX]
            self.length = message[RCPROTOLO_HEADER_SIZE_INDX]
        else:
            self.destination = destination
            self.origin = origin
            self.type = type
            self.length = length
        format = "<BBBB"
        self.packed = bytestring = struct.pack(format, self.destination, self.origin, self.type, self.length)
    
class RCProtocolSetHour:
    def __init__(self, header:RCProtocolHeader, time:int):
        self.header = header
        self.time = time
        format = "<i"
        time_packed = struct.pack(format, self.time)
        self.packed = self.header.packed+time_packed

class RCProtocolSetScheduler:
    def __init__(self, header:RCProtocolHeader, actuator_id:int, scheduler:Scheduler):
        self.header = header
        self.actuator_id = actuator_id 
        self.scheduler = scheduler
        format = "<b"
        actuator_packed = struct.pack(format, self.actuator_id)
        self.packed = self.header.packed+actuator_packed+self.scheduler.packed
    
class RCProtocolSetRule:
    def __init__(self, header:RCProtocolHeader, actuator_id:int, rule:Rule):
        self.header = header
        self.actuator_id = actuator_id 
        self.rule = rule
        format = "<b"
        actuator_packed = struct.pack(format, self.actuator_id)
        self.packed = self.header.packed+actuator_packed+self.rule.packed

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
        self.duration = duration #minutes
        format = "<BB" 
        info_packed = struct.pack(format, self.actuator_id, self.duration)
        self.packed = self.header.packed + info_packed

def rc_protocol_handle_received_msg(message):
    """ Translate the protocol message

    Args:
        message (_type_): _description_
    """
    
    # First bytes are the header
    header = RCProtocolHeader(message=message)
    print(header)
    
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
        print(f"RCPROTOCOL_MSG_SEND_MEASURE received")
        received_measure =RCProtocolSendMeasure(
            message=message,
            header=header
        )
        
        sensor = dbSensor.objects.get(id=received_measure.header.origin)
        for measure in received_measure.get_measures():
            print(measure)
            measure_db = dbMeaseure(sensor = sensor,
                                type = measure[1],
                                value =  measure[0])
            #measure_db.save()

        pass
    elif (header.type == RCPROTOCOL_MSG_MANUAL_ACTIVATION):
        #should not be received
        pass
    elif (header.type == RCPROTOCOL_MSG_ACTUATION_RULE) :
        #should not be received
        pass

def test_receive_measure():
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

def test_protocol_send_schedule():
    #head 
    head = RCProtocolHeader(destination=2,
                        origin=0,
                        type=RCPROTOCOL_MSG_SET_SCHEDULER,
                        length=RCPROTOCOL_SET_SCHEDULER_SIZE)
    schedule = Scheduler(week_days= 0b1010101,
                         hour= 17,
                         minute=30)
    
    set_scheduler = RCProtocolSetScheduler(header=head,
                                           scheduler=schedule,
                                           actuator_id=2)
    print(set_scheduler.packed)
    cadena_hexadecimal = ' '.join(['{:02x}'.format(byte) for byte in set_scheduler.packed])
    print(cadena_hexadecimal)

def test_protocol_set_hour():
    head = RCProtocolHeader(destination=2,
                    origin=0,
                    type=RCPROTOCOL_MSG_SET_TIME,
                    length=RCPROTOCOL_SET_SCHEDULER_SIZE)
    sethour = RCProtocolSetHour(header=head,
                                time = int(time.time()))
    print(sethour.packed)
    cadena_hexadecimal = ' '.join(['{:02x}'.format(byte) for byte in sethour.packed])
    print(cadena_hexadecimal)
    print(time.time())

def test_protocol_manual_activation():
    head = RCProtocolHeader(destination=2,
                origin=0,
                type=RCPROTOCOL_MSG_SET_TIME,
                length=RCPROTOCOL_SET_SCHEDULER_SIZE)
    manual_activation = RCProtocolManualActivation(header = head,
                                                   actuator_id= 2,
                                                   duration= 15) 
    print(manual_activation.packed)
    cadena_hexadecimal = ' '.join(['{:02x}'.format(byte) for byte in manual_activation.packed])
    print(cadena_hexadecimal)
    
def test_rc_protocol_handle_received_msg():

    msg_str = "00 02 04 09 01 00 00 20 41 01"
    msg = bytes.fromhex(msg_str)
    rc_protocol_handle_received_msg(msg)

