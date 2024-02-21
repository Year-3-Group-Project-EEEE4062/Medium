from machine import Pin, Timer
import utime
import uctypes
import struct

from displayInfo import oledDisplay
from bleFeature import mediumBLE
from mediumDataStorage import mediumStorage
from processMessages import processMssg
from rfTransmitter import mediumRF
from loraTransmitter import mediumLoRa

##################################################################
##################################################################
## Callback when data received through BLE
def receivedBLE(data):
    # Expected data to be received is utf-8
    print("Received: ", data)

    mode = processor.process(data)

    oledscreen.actionMssg("No",mode)

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
## Initialization

# Create instances
oledscreen = oledDisplay()
# sdCard = mediumStorage()

bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)
processor = processMssg()

# nrfModule = mediumRF()
# loraModule = mediumLoRa()

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# Infinite loop
while True:
    # check if BLE connected or not
    if bluetoothLowEnergy.is_connected():
        pass

# loraModule.loraSenderTest()
