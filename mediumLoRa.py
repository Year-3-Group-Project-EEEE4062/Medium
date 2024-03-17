import time
import struct
from lib.LoRa.ulora import LoRa, SPIConfig

# Client is the sender
# Server is the receiver

class LoRa_TX:
    def __init__(self):
    # Lora Parameters
        RFM95_RST = 17 # RST GPIO Pin
        RFM95_SPIBUS = SPIConfig.tx # SPI0
        RFM95_CS = 5 # NSS GPIO Pin
        RFM95_INT = 16 # Interrupt GPIO Pin (DIO0)
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 243
        self.SERVER_ADDRESS = 189

        # initialise radio
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.CLIENT_ADDRESS, RFM95_CS,
                     reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, 
                     acks=True)

    def loraTX(self, data):
        self.lora.send_to_wait(data, self.SERVER_ADDRESS)

class LoRa_RX:
    def __init__(self):
        # for debugging purposes during testing
        self.counter = 0

        # Lora Parameters
        RFM95_RST = 19 # RST pin
        RFM95_SPIBUS = SPIConfig.rx
        RFM95_CS = 1 # NSS pin 
        RFM95_INT = 18 #DIO0 pin
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 253
        self.SERVER_ADDRESS = 199

        # initialise radio
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.SERVER_ADDRESS, RFM95_CS, 
                        reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, 
                        acks=True)

    def loraRX(self, rx_cb):
        # set callback (overwriting exisiting callback)
        self.lora.on_recv = rx_cb

        # set to listen continuously
        self.lora.set_mode_rx()

class mediumLoRa:
    def __init__(self, bleSendCallback):
        # Timeout to get ack message from boat
        self.pingTimeout = 0.5

        # To know if a send is acknowledged or not
        self.boatPinged = False

        # To determine if there is a message to be sent
        self.flag = False

        self.ble_cb = bleSendCallback

        # Create instances of each tx and rx class
        self.mediumLoRa_TX = LoRa_TX()
        self.mediumLoRa_RX = LoRa_RX()

        # Initialize interrupt listener for LoRa
        # pass callback function to it
        self.mediumLoRa_RX.loraRX(self.rx_cb)

    # LoRa interrupt receiver callback function
    def rx_cb(self, payload):
        if(payload.message.decode() == '!'):
            self.boatPinged = True
        else:
            # Temporary as not all other data received will notify app
            self.ble_cb(payload.message)
        # Either way, able to communicate with boat

    # LoRa sender and wait for acknowledgement
    def sendForAck(self):
        # Indicate it has been transferred
        self.flag = False

        # Send data through LoRa
        self.mediumLoRa_TX.loraTX(self.mssgForSent)

        start = time.time()
        while time.time() - start < self.pingTimeout:
            if self.boatPinged:
                # Reset ack bool variable
                self.boatPinged = False
                return 'Y'
        
        self.boatPinged = False
        return 'N'

    def queueForTransfer(self, mssg, mode):
        self.mssgForSent = mssg
        self.mode = mode
        self.flag = True

    def getMode(self):
        return self.mode

    def checkLoRaFlag(self):
        return self.flag





