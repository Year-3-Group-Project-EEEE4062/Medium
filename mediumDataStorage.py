from machine import Pin, SPI
from lib.MicroSD import sdcard
import os

class mediumStorage:
    def __init__(self):
        # Depends if user wants to write data to new file or not
        self.createNewFile = False

        # Variables for filename
        self.extension = ".csv"
        self.mountDirectory = "/sd/"

        # Set the SPI pins of the adapter
        spi=SPI(1,baudrate=40000000,sck=Pin(10),mosi=Pin(11),miso=Pin(12))

        # Create instance of sdcard class from driver library
        sdAdapter=sdcard.SDCard(spi,cs = Pin(13))
        print("SD Adapter initialized!!")

        # Create a instance of MicroPython Unix-like Virtual File System (VFS),
        vfs=os.VfsFat(sdAdapter)

        # Mount the SD card
        os.mount(sdAdapter,'/sd')

        # Debug print SD card directory and files
        print(os.listdir('/sd'))

    def writetoSDTest(self, fileName, data):
        # Have a lot to edit in this section to suit application

        # Create the full filename directory 
        fullDirectory = self.mountDirectory+fileName+self.extension

        # Create / Open a file in write mode.
        # Write mode creates a new file.
        # If  already file exists. Then, it overwrites the file.
        f = open(fullDirectory,"w")

        # Write sample text
        for i in data:
            try:
                f.write(str(i))
                f.write(",")
                
            except OSError:
                print("Error when trying to write!!")
        
        # Write new line for next set of data
        try:
            f.write("\r\n")
        except OSError:
            print("Error when trying to create new line!!")

        print("Finished writing to sdCard!!")

        # Close the file
        f.close()



        


