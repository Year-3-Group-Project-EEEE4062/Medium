from machine import Pin, SPI
from lib.MicroSD import sdcard
import os

# Initialize the SD card
spi=SPI(1,baudrate=40000000,sck=Pin(10),mosi=Pin(11),miso=Pin(12))
sd=sdcard.SDCard(spi,Pin(13))

# Create a instance of MicroPython Unix-like Virtual File System (VFS),
vfs=os.VfsFat(sd)

# Mount the SD card
os.mount(sd,'/sd')