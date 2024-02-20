"""Test for nrf24l01 module.  Portable between MicroPython targets."""

import usys
import ustruct as struct
import utime
import uctypes
from machine import Pin, SPI, SoftSPI
from lib.rf.nrf24l01 import NRF24L01
from micropython import const

# Run nrf24l01test.responder() on responder, then nrf24l01test.initiator() on initiator

# Responder pause between receiving data and checking for further packets.
_RX_POLL_DELAY = const(15)

# Responder pauses an additional _RESPONER_SEND_DELAY ms after receiving data and before
# transmitting to allow the (remote) initiator time to get into receive mode. The
# initiator may be a slow device. Value tested with Pyboard, ESP32 and ESP8266.
_RESPONDER_SEND_DELAY = const(10)

class mediumRF:
    def __init__(self):
        self.timeoutTime = 250
        
        # Set the pins for the RF module
        self.spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
        self.cfg = {"spi": self.spi, "miso": 4, "mosi": 7, "sck": 6, "csn": 5, "ce": 8}

        # Addresses are in little-endian format. They correspond to big-endian
        # 0xf0f0f0f0e1, 0xf0f0f0f0d2
        self.pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

        self.csn = Pin(self.cfg["csn"], mode=Pin.OUT, value=1)
        self.ce = Pin(self.cfg["ce"], mode=Pin.OUT, value=0)
        self.spi = self.cfg["spi"]
        self.nrf = NRF24L01(self.spi, self.csn, self.ce, payload_size=32)

        self.nrf.open_tx_pipe(self.pipes[0])
        self.nrf.open_rx_pipe(1, self.pipes[1])

    def sender(self, rfMssg):
        # Variable to keep track of how many trials
        num_needed = 1
        num_failures = 0

        print("NRF24L01 initiator mode, %d attempts" % num_needed)

        # Start loop to attempt to send messages
        while num_failures < num_needed:
            # stop listening and send packet
            self.nrf.stop_listening()

            # Assign the message to a local variable
            print("sending..")
            
            # Send the message through RF
            try:
                # Send the mesage directly without needing to encode
                self.nrf.send(rfMssg)
            except OSError:
                # Commonly hardware error
                pass

            # start listening again
            self.nrf.start_listening()

            # wait for response, with 250ms timeout
            start_time = utime.ticks_ms()
            timeout = False

            # Track the time to wait for a response for 250ms
            while not self.nrf.any() and not timeout:
                if utime.ticks_diff(utime.ticks_ms(), start_time) > self.timeoutTime:
                    timeout = True

            # Check if got a response from the responder or not
            # Did not get a response
            if timeout:
                print("failed, response timed out")
                
                num_failures += 1

            # Obtained a response
            else:
                # recv packet
                pingedMssg = self.nrf.recv().decode('utf-8')

                print("Pinged Message: ", pingedMssg)                

                # Return "Yes" to indicate boat is within reach
                return "Yes"

                # Break the loop for transmitting since responder got the message
                break

            # delay then loop
            utime.sleep_ms(250)
        
        # Return "No" to indicate cannot be connected to boat
        return "No"

    def nrfSenderTest(self):
        while True:
            self.__doubleTest()
            self.__integerTest()

    def __doubleTest(self):
        # Can only send a maximum of 4 doubles per transmission
        dataToBeSent = [2.9438889,101.8735556]
        double_identifier = 0x01

        data = bytearray()
        data.extend(double_identifier.to_bytes(1, byteorder='big'))
        data.extend(struct.pack('d' * len(dataToBeSent), *dataToBeSent))
    
        self.sender(data)

    def __integerTest(self):
        # Can only send a maximum of 4 doubles per transmission
        dataToBeSent = [1,2,3,4,5,6,7,8]
        integer_identifier = 0x02

        data = bytearray()
        data.extend(integer_identifier.to_bytes(1, byteorder='big'))
        data.extend(struct.pack('i' * len(dataToBeSent), *dataToBeSent))

        self.sender(data)

