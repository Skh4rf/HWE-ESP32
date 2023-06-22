from machine import Pin
import time

Driver1 = Pin(16, Pin.OUT)
Signal	= Pin(13, Pin.IN, Pin.PULL_UP)

while True:
    Driver1.value(not Signal.value())
