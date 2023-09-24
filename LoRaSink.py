"""
Lora sink module, based at adafruit examples and library
This app receive and process LoRa comunication with the sensonrs and actuators modules
"""
# Import Python System Libraries
from operator import truediv
from datetime import datetime
import time
# Import Blinka Libraries to control the raspberry
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x to control LoRa comunication
import adafruit_rfm9x
import struct
from enum import Enum

LORA_HEADER_SIZE = 4
LORA_SINK_ADDR = 0
LORA_RECEIVER_INDX = 0
LORA_SENDER_INDX = 1
LORA_MSG_PROTOCOL_INDX = 2
LORA_SIZE_INDX = 3

MSG_PROTOCOL_SEND_MEASURES = 4
PROTOCOL_MSG_SET_TIME = 1


def conf_buttons():

    # Button A
    btnA = DigitalInOut(board.D5)
    btnA.direction = Direction.INPUT
    btnA.pull = Pull.UP

    # Button B
    btnB = DigitalInOut(board.D6)
    btnB.direction = Direction.INPUT
    btnB.pull = Pull.UP

    # Button C
    btnC = DigitalInOut(board.D12)
    btnC.direction = Direction.INPUT
    btnC.pull = Pull.UP
    return btnA, btnB, btnC


def conf_Lora():
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 868.0)
    rfm9x.tx_power = 23
    return rfm9x


def main():
    btnA, btnB, btnC = conf_buttons()
    print("main")
    rfm9x = conf_Lora()
    main_running = True
    packet = None
    print("esperar paquete")
    while main_running:
        packet = rfm9x.receive(with_header=True)
        if packet:
            print(f"Size of packet {len(packet)}")
            receiver = packet[LORA_RECEIVER_INDX]
            sender = packet[LORA_SENDER_INDX]
            size = packet[LORA_SIZE_INDX]
            protocol = packet[LORA_MSG_PROTOCOL_INDX]
            print(
                f"receiver {receiver} sender {sender} size {size} protocol {protocol}")
            if (protocol == PROTOCOL_MSG_SET_TIME):
                print("Time petition received")
                unpack_code = "<" + "i"
                device_time = struct.unpack(
                    unpack_code, packet[LORA_HEADER_SIZE:])[0]
                current_time = int(datetime.now().timestamp())

                print(f"Device time: {device_time}")
                print(f"Current time: {current_time}")
                print(f"Diff time: {current_time-device_time}")

                header = {
                    "destination": 5,
                    "origin": 1,
                    "type": 1,
                    "length": 8,
                }
                time.sleep(2)
                rfm9x.send(
                    destination=header["destination"],
                    node=header["origin"],
                    identifier=header["type"],
                    flags=header["length"],
                    data=struct.pack("<i", current_time)
                )

            if (protocol == MSG_PROTOCOL_SEND_MEASURES):
                print("measures received")
                print(f"measure size {len(packet[LORA_HEADER_SIZE:])}")
                print("".join('{:02x} '.format(x)
                      for x in packet[LORA_HEADER_SIZE:]))
                try:

                    unpack_code = "<" + "Bf"*int(size/5)
                    print(unpack_code)
                    print(packet[LORA_HEADER_SIZE-1:])
                    measures = struct.unpack(
                        unpack_code, packet[LORA_HEADER_SIZE:])
                    print(measures)
                except Exception as e:
                    print("Formato no adecuado")
                    print(e)


if __name__ == "__main__":
    main()
