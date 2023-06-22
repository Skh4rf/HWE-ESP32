from machine import Pin
import time

# Define I2C pins and create I2C object
Driver1 = Pin(16, Pin.OUT)
Driver2 = Pin(17, Pin.OUT)
Driver3 = Pin(18, Pin.OUT)
Driver4 = Pin(19, Pin.OUT)
ButtonIncrease = Pin(21, Pin.IN, Pin.PULL_UP)
ButtonDecrease = Pin(22, Pin.IN, Pin.PULL_UP)
dutyCycle = 0.5

while True:
    if not ButtonIncrease.value() and dutyCycle < 1:
        dutyCycle += 0.05
        print(str(dutyCycle))
        time.sleep(0.005)
        while not ButtonIncrease.value():
            pass
    if not ButtonDecrease.value() and dutyCycle > 0:
        dutyCycle -= 0.05
        print(str(dutyCycle))
        time.sleep(0.005)
        while not ButtonDecrease.value():
            pass
    Driver1.value(1)
    Driver2.value(1)
    Driver3.value(1)
    Driver4.value(1)
    time.sleep(0.005*dutyCycle)
    Driver1.value(0)
    Driver2.value(0)
    Driver3.value(0)
    Driver4.value(0)
    time.sleep(0.005*(1-dutyCycle))

