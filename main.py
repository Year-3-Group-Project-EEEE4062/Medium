from machine import Pin
from time import sleep

#nrf24l01_test.responder()

led = Pin('LED', Pin.OUT)
print('Blinking LED Example')

while True:
  led.value(not led.value())
  sleep(0.5)



