"""
This file contais the classes and functions needed for riegocontrol protocol handling.
"""
import struct

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
        self.measures = struct.unpack(
                        self.unpack_code, self.message[RCPROTOLO_HEADER_SIZE+1:])
    
    def get_measures_num(self) -> int:
        return self.measures_num
    
    def get_measures(self) -> list[Measure]:
        return self.measures


class RCProtocolManualActivation:
    def __init__(self, header:RCProtocolHeader, actuator_id:int, duration:int):
        self.header = header
        self.actuator_id = actuator_id
        self.duration = duration

def rc_protocol_handle(message):
    """ Translate the protocol message

    Args:
        message (_type_): _description_
    """
    
    # First bytes are the header
    header = RCProtocolHeader(message=message)
    
    
    if (header.type == RCPROTOCOL_NONE):
        pass
    elif (header.type == RCPROTOCOL_MSG_SET_TIME):
        pass
    elif (header.type == RCPROTOCOL_MSG_DEFAULT_RULE):
        pass
    elif (header.type == RCPROTOCOL_MSG_SET_SCHEDULER):
        pass
    elif (header.type == RCPROTOCOL_MSG_SEND_MEASURE):
        pass
    elif (header.type == RCPROTOCOLMSG_MANUAL_ACTIVATION):
        pass
    elif (header.type == RCPROTOCOL_MSG_ACTUATION_RULE) :
        pass