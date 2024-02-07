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

# Set the pins for the RF module
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
cfg = {"spi": spi, "miso": 4, "mosi": 7, "sck": 6, "csn": 5, "ce": 8}

# Addresses are in little-endian format. They correspond to big-endian
# 0xf0f0f0f0e1, 0xf0f0f0f0d2
pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")


def initiator(rfMssg):
    csn = Pin(cfg["csn"], mode=Pin.OUT, value=1)
    ce = Pin(cfg["ce"], mode=Pin.OUT, value=0)
    spi = cfg["spi"]
    nrf = NRF24L01(spi, csn, ce, payload_size=8)

    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    # Variable to keep track of how many trials
    num_needed = 16
    num_failures = 0

    print("NRF24L01 initiator mode, %d attempts" % num_needed)

    while num_failures < num_needed:
        # stop listening and send packet
        nrf.stop_listening()

        # Assign the message to a local variable
        mssg = rfMssg
        print("sending:", mssg)
        
        # Send the message through RF
        try:
            nrf.send(mssg.encode('utf-8'))
        except OSError:
            # Commonly hardware error
            pass

        # start listening again
        nrf.start_listening()

        # wait for response, with 250ms timeout
        start_time = utime.ticks_ms()
        timeout = False

        # Track the time to wait for a response for 250ms
        while not nrf.any() and not timeout:
            if utime.ticks_diff(utime.ticks_ms(), start_time) > 250:
                timeout = True

        # Check if got a response from the responder or not
        # Did not get a response
        if timeout:
            print("failed, response timed out")
            num_failures += 1

        # Obtained a response
        else:
            # recv packet
            pingedMssg = nrf.recv().decode('utf-8')

            print("Pinged Message: ", pingedMssg)

            # Break the loop for transmitting since responder got the message
            break

        # delay then loop
        utime.sleep_ms(250)

    print("initiator finished sending; attempts = %d" % (num_failures+1))
