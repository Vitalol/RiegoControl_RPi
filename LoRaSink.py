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

import threading
import socket
import os
import sensors.rc_protocol as RCP


LORA_HEADER_SIZE = 4
LORA_SINK_ADDR = 0
LORA_RECEIVER_INDX = 0
LORA_SENDER_INDX = 1
LORA_MSG_PROTOCOL_INDX = 2
LORA_SIZE_INDX = 3

MSG_PROTOCOL_SEND_MEASURES = 4
PROTOCOL_MSG_SET_TIME = 1

lora_semaphore = threading.Lock()

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

def lora_sender(lora):
    """Esta tarea recibe la comunicación por socket y envía los datos.
    """
    # Definir la dirección IP y el puerto del servidor
    IP = "127.0.0.1"  # Dirección IP local del servidor
    PUERTO = 54321    # Puerto para la comunicación

    # Crear el socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincular el socket a la dirección y puerto
    server_socket.bind((IP, PUERTO))

    # Establecer el límite máximo de conexiones pendientes en la cola
    server_socket.listen(1)

    print("Esperando conexiones...")

    while True:
        # Aceptar conexiones entrantes
        client_socket, client_address = server_socket.accept()

        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024)
            if data:
                print(f"Datos recibidos del cliente: {data.hex()}")
                with lora_semaphore:
                    lora.send(
                        destination= data[0],   # destination
                        node=data[1],          # origin
                        identifier=data[2],    # type
                        flags=data[3],         # length
                        data=data[4:]
                    )

        finally:
            # Cerrar la conexión con el cliente
            client_socket.close()


def lora_receiver(lora):
    """Esta tarea va recibiendo lecturas 
    """

    print("LoRa RX")
    lora_rx_running = True
    packet = None
    print("esperar paquete")
    while lora_rx_running:
        with lora_semaphore:
            packet = lora.receive(with_header=True)
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
                    "destination": 1,
                    "origin": 1,
                    "type": 1,
                    "length": 8,
                }
                time.sleep(2)
                with lora_semaphore:
                    lora.send(
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



def main():


       # is equal to threading.Semaphore(1)


    rfm9x = conf_Lora()
    sender_thread = threading.Thread(target=lora_sender, args = (rfm9x,))
    receiver_thread = threading.Thread(target=lora_receiver, args = (rfm9x,))

    sender_thread.start()
    receiver_thread.start()



if __name__ == "__main__":
    main()
