from machine import Pin, SPI
from lib.MicroSD import sdcard
import random
import os

# Only take out or insert the MicroSD card when Medium is power OFF
# Otherwise, the Medium will have problem detecting the MicroSD card

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
        # print("SD Adapter initialized!!")

        # Create a instance of MicroPython Unix-like Virtual File System (VFS),
        vfs=os.VfsFat(sdAdapter)

        # Mount the SD card
        os.mount(sdAdapter,'/sd')

        # Debug print SD card directory and files
        # print(os.listdir('/sd'))

    def writeToStorage(self, data):
        fileName = "BLE_Range Test"
        header = ["RSSI", "Latitude", "Longitude"]

        # Create the full filename directory 
        fullDirectory = self.mountDirectory+fileName+self.extension


        with open(fullDirectory,"w") as f:
            # Write the header of the file
            for i in header:
                try:
                    f.write(i)
                    f.write(",")
                    
                except OSError:
                    print("Error when trying to write!!")
            
            # Write new line
            try:
                f.write("\r\n")
            except OSError:
                print("Error when trying to create new line!!")

            # Write data to the csv file
            for row in data:
                for column in row:
                    # Write a row of data
                    try:
                        f.write(str(column))
                        f.write(",")
                        
                    except OSError:
                        print("Error when trying to write!!")
                
                # Write new line for next row of data
                try:
                    f.write("\r\n")
                except OSError:
                    print("Error when trying to create new line!!")
        
        print("Saved file!!")

    def __generateRandomDataset(self):
        # Generate random data for each column
        return [
            f"{random.randint(1, 31):02}/{random.randint(1, 12):02}/{random.randint(2000, 2024)}",
            f"{random.randint(0, 23):02}:{random.randint(0, 59):02}",
            round(random.uniform(100.0, 180.0), 6),  # Longitude
            round(random.uniform(-90.0, 90.0), 6),  # Latitude
            round(random.uniform(0.0, 100.0), 2),  # Full Depth
            round(random.uniform(10.0, 30.0), 2),  # 1/3 Depth (Celcius)
            round(random.uniform(10.0, 30.0), 2),  # 2/3 Depth (Celcius)
            round(random.uniform(10.0, 30.0), 2)   # 3/3 Depth (Celcius)
        ]

    def writetoSDTest(self):
        # the number of random rows of data to generate
        num_rows = 5

        # Have a lot to edit in this section to suit application
        fileName = "MicroSD_Test"
        header = ["Date (dd/mm/yyyy)", "Time (m:s)", "Longitude", "Latitude", "Full Depth (m)", "1/3 Depth (Celcius)", "2/3 Depth (Celcius)", "3/3 Depth (Celcius)"]
        data = [self.__generateRandomDataset() for _ in range(num_rows)]
        print(data)

        # Create the full filename directory 
        fullDirectory = self.mountDirectory+fileName+self.extension

        # Create / Open a file in write mode.
        # Write mode creates a new file.
        # If already file exists. Then, it overwrites the file.
        with open(fullDirectory,"w") as f:
            # Write the header of the file
            for i in header:
                try:
                    f.write(i)
                    f.write(",")
                    
                except OSError:
                    print("Error when trying to write!!")
            
            # Write new line
            try:
                f.write("\r\n")
            except OSError:
                print("Error when trying to create new line!!")

            # Write data to the csv file
            for row in data:
                for column in row:
                    # Write a row of data
                    try:
                        f.write(str(column))
                        f.write(",")
                        
                    except OSError:
                        print("Error when trying to write!!")
                
                # Write new line for next row of data
                try:
                    f.write("\r\n")
                except OSError:
                    print("Error when trying to create new line!!")

        print("Finished writing to sdCard!!")



        


