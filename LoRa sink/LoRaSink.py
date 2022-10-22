"""
Lora sink module, based at adafruit examples and library
This app receive and process LoRa comunication with the sensonrs and actuators modules
"""
# Import Python System Libraries
from operator import truediv
import time
# Import Blinka Libraries to control the raspberry
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x to control LoRa comunication
import adafruit_rfm9x

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
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power = 23
    prev_packet = None
    return rfm9x

def main():
    btnA, btnB, btnC = conf_buttons()
    rfm9x = conf_Lora()
    main_running = True
    packet = None
    while main_running:
        packet = rfm9x.receive(with_header=True)
        if packet:
            print(packet)


if __name__ == "__main__":
    main()
