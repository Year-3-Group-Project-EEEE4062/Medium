from machine import Pin, SoftI2C
from lib.OLED import ssd1306



#defining a class for OLED display
class display:
    #constructor
    def __init__(self):
        #Combination of I2C pins used for OLED
        self.i2c = SoftI2C(scl=Pin(21), sda=Pin(20))
        
        #defining class variables
        self.oled_width = 128
        self.oled_height = 64

        #create an instance
        self.oled = ssd1306.SSD1306_I2C(self.oled_width, self.oled_height, self.i2c)

    def showInfo(self):
        self.oled.fill(0) # clear the screen
        self.oled.text('Hello, World 1!', 0, 0)
        self.oled.text('Hello, World 3!', 0, 10)
        self.oled.show()



