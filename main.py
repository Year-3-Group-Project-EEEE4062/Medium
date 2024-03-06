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
        pinged = LoRa.sendForAck(data)
        oledscreen.actionMssg(pinged, mode)
    
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

def bleTtest():
    # Infinite loop
    while True:
        # check if BLE connected or not
        if bluetoothLowEnergy.is_connected():
            pass

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

oledscreen.welcomeMssg()
# loraModule_RX.loraRX()

# Test Functions
bleTtest()
# loraModule.loraSenderTest()
# sdCard.writetoSDTest()

