from machine import Pin, SoftI2C
from lib.OLED import ssd1306
import utime

#defining a class for OLED display
class mediumDisplay:
    #constructor
    def __init__(self):
        #Combination of I2C pins used for OLED
        self.i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
        
        #defining class variables
        self.oled_width = 128
        self.oled_height = 64

        #create an instance
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)

    def welcomeMssg(self):
        #print initialized message
        self.oled.fill(0)
        self.oled.text("Medium Started", 0, 10)
        self.oled.text("Ready...", 0, 30)
        self.oled.text("Use Arfanify!", 0, 50)
        self.oled.show()

    def disconnectedMssg(self):
        self.oled.fill(0)
        self.oled.text("Disconnected...", 0, 10)
        self.oled.text("Reconnect to", 0, 30)
        self.oled.text("Arfanify", 0, 40)
        self.oled.show()

    def connectedMssg(self):
        self.oled.fill(0)
        self.oled.text("Connected...", 0, 10)
        self.oled.text("Stay safe!!", 0, 30)
        self.oled.show()

    def microSDProblemMssg(self):
        self.oled.fill(0)
        self.oled.text("MicroSD Failed!", 0, 10)
        self.oled.text("OFF Medium, ", 0, 30)
        self.oled.text("Then ON Medium", 0, 50)
        self.oled.show()

    def displayProblemMssg(self):
        self.oled.fill(0)
        self.oled.text("OLED Failed!", 0, 10)
        self.oled.text("OFF Medium, ", 0, 30)
        self.oled.text("Then ON Medium", 0, 50)
        self.oled.show()

    def loraProblemMssg(self):
        self.oled.fill(0)
        self.oled.text("LoRa Failed!", 0, 10)
        self.oled.text("OFF Medium, ", 0, 30)
        self.oled.text("Then ON Medium", 0, 50)
        self.oled.show()

    def bleProblemMssg(self):
        self.oled.fill(0)
        self.oled.text("BLE Failed!", 0, 10)
        self.oled.text("OFF Medium, ", 0, 30)
        self.oled.text("Then ON Medium", 0, 50)
        self.oled.show()

    def actionMssg(self, boatStatus, mode):
        self.oled.fill(0)

        self.oled.text("Boat Ping: ", 0, 10)
        self.oled.text(boatStatus, 85, 10)

        self.oled.text("Mode     : ", 0, 25)
        self.oled.text(mode, 85, 25)

        # Get the current time (local time)
        current_time = utime.localtime()
        # Extract the hour and minute
        hour, minute = current_time[3], current_time[4]

        if (hour<10):
            stringHours = "0"+str(hour)
        else:
            stringHours = str(hour)

        if (minute<10):
            stringMinutes = "0"+str(minute)
        else:
            stringMinutes = str(minute)
        
        stringTime = stringHours+":"+stringMinutes

        self.oled.text("Last Time: ", 0, 40)
        self.oled.text(stringTime, 85, 40)

        self.oled.show()
        







