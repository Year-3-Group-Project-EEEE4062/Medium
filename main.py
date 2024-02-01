from displayInfo import display
from time import sleep_ms

oledscreen = display()
sleep_ms(1000)
oledscreen.connectedMssg()
