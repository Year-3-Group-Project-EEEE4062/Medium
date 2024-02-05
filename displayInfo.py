from machine import Pin, SoftI2C
from lib.OLED import ssd1306

#defining a class for OLED display
class oledDisplay:
    #constructor
    def __init__(self):
        #Combination of I2C pins used for OLED
        self.i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
        
        #defining class variables
        self.oled_width = 128
        self.oled_height = 64

        #create an instance
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)

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

    def actionMssg(self, bleMssg):
        self.oled.fill(0)
        self.oled.text("Action: ", 0, 10)
        self.oled.text(bleMssg, 60, 10)
        self.oled.show()
        







