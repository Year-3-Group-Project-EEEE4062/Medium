import utime
import struct
from lib.LoRa.ulora import LoRa, ModemConfig, SPIConfig

# Client is the sender
# Server is the receiver

class mediumLoRa:
    def __init__(self):
    # Lora Parameters
        RFM95_RST = 3 # RST GPIO Pin
        RFM95_SPIBUS = SPIConfig.rp2_0 # SPI0
        RFM95_CS = 5 # NSS GPIO Pin
        RFM95_INT = 2 # Interrupt GPIO Pin (DIO0)
        RF95_FREQ = 433.0
        RF95_POW = 20
        self.CLIENT_ADDRESS = 253
        self.SERVER_ADDRESS = 199

        # initialise radio
        self.lora = LoRa(RFM95_SPIBUS, RFM95_INT, self.CLIENT_ADDRESS, RFM95_CS,
                     reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, 
                     acks=True)

    def __doubleTest(self):
        # Can only send a maximum of 4 doubles per transmission
        dataToBeSent = [2.9438889,101.8735556]
        double_identifier = 0x01

        data = bytearray()
        data.extend(double_identifier.to_bytes(1,'big')) # data type identifier
        data.extend(struct.pack('i', len(dataToBeSent))) # how many data to extracted
        data.extend(struct.pack('d' * len(dataToBeSent), *dataToBeSent)) # the data itself

        print(data)
        return data

    def loraSenderTest(self):
        counter = 0

        while True:
            # get practice message
            data = self.__doubleTest()
            self.lora.send_to_wait(data, self.SERVER_ADDRESS)
            print("Data type: ", type(data))
            counter = counter + 1
            print("sent LoRa message No.",counter,"!")
            utime.sleep_ms(500)