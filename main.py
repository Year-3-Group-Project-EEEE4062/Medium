from machine import Pin
import utime

from displayInfo import oledDisplay
from bleFeature import mediumBLE
from mediumDataStorage import mediumStorage
from processMessages import processMssg
import mediumLoRa

##################################################################
##################################################################
## Callback when data received through BLE
def receivedBLE(data):
    # Process the received BLE message
    mode = processor.process(data)

    # Send BLE data to boat through LoRa
    loraModule_TX.loraTX(data)

    oledscreen.actionMssg("No", mode)

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
try:
    sdCard = mediumStorage()
    print("Medium MicroSD Initialized!")
except OSError:
    oledscreen.microSDProblemMssg()


bluetoothLowEnergy = mediumBLE(connectedBLE, disconnectedBLE, receivedBLE)
print("Medium BLE Initialized!!")

processor = processMssg() 

loraModule_TX = mediumLoRa.mediumLoRa_TX()
print("Medium LoRa TX initialized!!")

# loraModule_RX = mediumLoRa.mediumLoRa_RX()
# print("Medium LoRa RX initialized!!")

# Setup on board LED to let user know also if BLE connected or not 
led = Pin("LED", Pin.OUT)
led.off()

##################################################################
## main operation

# loraModule_RX.loraRX()

# Test Functions
bleTtest()
# loraModule.loraSenderTest()
# sdCard.writetoSDTest()

