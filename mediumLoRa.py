import utime
import struct
from lib.LoRa.ulora import LoRa, SPIConfig

# Client is the sender
# Server is the receiver

class mediumLoRa_TX:
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
        ack = self.lora.send_to_wait(data, self.SERVER_ADDRESS)
        print(ack)

class mediumLoRa_RX:
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

    def loraRX(self):
        # set callback (overwriting exisiting callback)
        self.lora.on_recv = self.testCallback

        # set to listen continuously
        self.lora.set_mode_rx()

    def __extractData(self, buf):
        # data type identifier
        integer_identifier = 0x01
        double_identifier = 0x02

        # Essentials for decoding message
        mssgStartingIndex = 6
        intBufferSize = 4
        doubleBufferSize = 8

        dataType_identifier = mssg[1]
        
        # Get the length of the information
        dataLength = struct.unpack('i', mssg[2:mssgStartingIndex])[0]

        if dataType_identifier == double_identifier:
            double_value = struct.unpack('d'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(doubleBufferSize*dataLength)])
            print(double_value)
            return double_value

        elif dataType_identifier == integer_identifier:
            print(len( mssg[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)]))
            integer_value = struct.unpack('i'* dataLength, mssg[mssgStartingIndex:mssgStartingIndex+(intBufferSize*dataLength)])
            print(integer_value)
            return integer_value

        else:
            raise ValueError("Unknown identifier")
        
    def testCallback(self, payload):
        self.counter = self.counter + 1
        print("******************************************")
        print("From:", payload.header_from)
        print("Message No.",self.counter)
        print("Received:", self.__extractData(payload.message))
        print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
        pass

    def loraReceiverTest(self):
        # set callback (overwriting exisiting callback)
        self.lora.on_recv = self.testCallback

        # set to listen continuously
        self.lora.set_mode_rx()

        # loop and wait for data
        while True:
            utime.sleep_ms(10)
