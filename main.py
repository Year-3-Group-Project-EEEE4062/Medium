from machine import Pin
import utime

from displayInfo import oledDisplay
from bleFeature import mediumBLE
from mediumDataStorage import mediumStorage
from processMessages import processMssg
from mediumLoRa import mediumLoRa

##################################################################
##################################################################
## Callback when data received through BLE
def receivedBLE(data):
    # Process the received BLE message
    mode = processor.process(data)

    # Send BLE data to boat through LoRa
    # But never send time info for RTC as boat pico w dont need it
    if mode != "I":
        LoRa.queueForTransfer(data, mode)

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
oledscreen = oledDisplay()
print("Medium Display Initialized!")

# MicroSD Adapter more prone to failing
while True:
    try:
        sdCard = mediumStorage()
        print("Medium MicroSD Initialized!")
        break
    except OSError:
        oledscreen.microSDProblemMssg()


bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)
print("Medium BLE Initialized!!")

processor = processMssg() 
LoRa = mediumLoRa()
print("Medium LoRa initialized!!")

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# Test Functions
# loraModule.loraSenderTest()
# sdCard.writetoSDTest()

oledscreen.welcomeMssg()

# Infinite loop
while True:
    # check if there is a message to be sent or not
    if LoRa.checkLoRaFlag():
        print("##################################################################")
        print("New data to be sent!!")
        pinged = LoRa.sendForAck()
        mode = LoRa.getMode()
        oledscreen.actionMssg(pinged, mode)


