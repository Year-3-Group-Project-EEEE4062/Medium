from machine import Pin
import utime

from mediumDisplay import mediumDisplay
from mediumBLE import mediumBLE
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

def notifyBLE(data):
    bluetoothLowEnergy.send(data)
    print("Notified: ",data)

##################################################################
## Callback when BLE connected to phone
def connectedBLE():
    print("Connected")
    oledscreen.connectedMssg()

    # Turn ON onboard LED
    # This to indicate to user that BLE is connected
    led.on()

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
while True:
    try:
        oledscreen = mediumDisplay()
        print("Medium Display Initialized!")
        break
    
    except:
        oledscreen.displayProblemMssg()

while True:
    try:
        bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)
        print("Medium BLE Initialized!!")
        break
    
    except:
        oledscreen.bleProblemMssg()

while True:
    try:
        processor = processMssg() 
        LoRa = mediumLoRa(notifyBLE)
        print("Medium LoRa initialized!!")
        break

    except:
        oledscreen.loraProblemMssg()

while True:
    try:
        # # MicroSD Adapter more prone to failing
        sdCard = mediumStorage()
        print("Medium MicroSD Initialized!")
        break

    except:
        oledscreen.microSDProblemMssg()

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# Test Functions
# loraModule.loraSenderTest()
# sdCard.writetoSDTest()

oledscreen.welcomeMssg()

try:
    # Infinite loop
    while True:
        # check if there is a message to be sent or not
        if LoRa.checkLoRaFlag():
            print("##################################################################")
            try:
                pinged = LoRa.sendForAck()
                mode = LoRa.getMode()
                oledscreen.actionMssg(pinged, mode)
            except:
                oledscreen.mainProblemMssg()
            
except KeyboardInterrupt:
    pass



