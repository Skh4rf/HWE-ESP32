from machine import Pin, I2C
import math
import time

RES_PIN = 26

text1 = bytearray(b"   Username:    ")
text2 = bytearray(b"      XXX       ")
text3 = bytearray(b"   Password:    ")
text4 = bytearray(b"      XXX       ")

slave2w = 0x3e
comsend = 0x00
datasend = 0x40
line2 = 0xC0

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

devices = i2c.scan()

print(devices)
print(str(len(devices)) + " Devices-Adresses detected")
    
def show(text):
    i2c.writeto(slave2w, bytes([datasend]) + text)

def nextline():
    i2c.writeto(slave2w, bytes([comsend, line2]))

def CiZ_init():
    i2c.writeto(slave2w, bytes([comsend, 0x38]))  # Function set: 8-bit data
    time.sleep_ms(10)
    i2c.writeto(slave2w, bytes([comsend, 0x39]))  # Function set: 8-bit data + instruction table 1
    time.sleep_ms(10)
    i2c.writeto(slave2w, bytes([comsend, 0x14]))  # Set OSC frequency
    i2c.writeto(slave2w, bytes([comsend, 0x78]))  # Set contrast
    i2c.writeto(slave2w, bytes([comsend, 0x5D]))  # Set ICON display ON | Booster ON | contrast
    i2c.writeto(slave2w, bytes([comsend, 0x6D]))  # Set follower circuit ON | Set follower ratio
    i2c.writeto(slave2w, bytes([comsend, 0x0C]))  # Set display ON
    i2c.writeto(slave2w, bytes([comsend, 0x01]))  # Clear display
    i2c.writeto(slave2w, bytes([comsend, 0x06]))  # Entry mode | Increment

    time.sleep_ms(10)

def setup():
    res_pin = Pin(RES_PIN, Pin.OUT)
    res_pin.value(1)
    time.sleep_ms(10)

def loop():
    CiZ_init()
    show(text1)
    nextline()
    show(text2)
    time.sleep(1)

    CiZ_init()
    show(text3)
    nextline()
    show(text4)
    time.sleep(1)

if 62 in devices:
    print("Display-Address found!")
    setup()
    while True:
        loop()
        
else:
    print("Display-Address NOT found!")