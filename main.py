from machine import Pin, Timer
import utime
import uctypes
import struct

from displayInfo import oledDisplay
from bleFeature import mediumBLE
from rfTransmitter import mediumRF
from mediumDataStorage import mediumStorage
from processMessages import processMssg

##################################################################
## Callback when data received through BLE
def receivedBLE(data):
    # Expected data to be received is utf-8
    print("Received: ", data)

    mode = processor.process(data)

    # directly give the coded data to the RF
    # boatStatus = nrfModule.sender(sendMsg)

    oledscreen.actionMssg("No",mode)
    # oledscreen.actionMssg(boatStatus,decoded_data)

##################################################################
## Callback when BLE connected to phone
def connectedBLE():
    print("Connected")
    oledscreen.connectedMssg()

    # Turn ON onboard LED
    # This to indicate to user that BLE is connected
    led.on()
    utime.sleep_ms(50)

##################################################################
## Callback when BLE disconnected from to phone
def disconnectedBLE():
    print("Disconnected")
    oledscreen.disconnectedMssg()

    # Turn OFF onboard LED
    # This to indicate to user that BLE NOT connected
    led.off()

##################################################################
##################################################################
## Start of main file

# Create instances
oledscreen = oledDisplay()
bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)
nrfModule = mediumRF()
processor = processMssg()
# sdCard = mediumStorage()

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

# Infinite loop
while True:
    # check if BLE connected or not
    if bluetoothLowEnergy.is_connected():
        continue
