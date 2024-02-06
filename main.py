from machine import Pin, Timer
import time
import uctypes

from displayInfo import oledDisplay
from bleFeature import mediumBLE
import rfFeature

def receivedBLE(data):
    # Expected data to be received is utf-8
    print("Received: ", data)

    # Decode the uint8 data received
    decoded_data = data.decode('utf-8')

    oledscreen.actionMssg(decoded_data)

def connectedBLE():
    print("Connected")
    oledscreen.connectedMssg()

    # Turn ON onboard LED
    # This to indicate to user that BLE is connected
    led.on()

def disconnectedBLE():
    print("Disconnected")
    oledscreen.disconnectedMssg()

    # Turn OFF onboard LED
    # This to indicate to user that BLE NOT connected
    led.off()

oledscreen = oledDisplay()
bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

#rfFeature.initiator()

while True:
    # check if BLE connected or not
    if bluetoothLowEnergy.is_connected():
        continue
