import machine
import time

# Define I2C pins and create I2C object
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

addr = 0x20

# MCP23008 Register addresses
DDR = 0x00   # I/O direction register
PORT = 0x09    # GPIO port register

def setOutput(data):
    # Set all pins as outputs
    i2c.writeto(addr, bytes([DDR, 0x00]))
    time.sleep(0.001)

    # Turn on all LEDs
    i2c.writeto(addr, bytes([PORT, data]))
    time.sleep(0.001)

# Blink the LEDs
while True:
    setOutput(0xFF)
    print("On")
    time.sleep(1)
    setOutput(0x00)
    print("Off")
    time.sleep(1)