import machine
import time

# Define I2C pins and create I2C object
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

addr = 0x4D  # ADC I2C address

def get_adc_value():
    # Read ADC value
    i2c.writeto(addr, bytes([0x00]))  # Start conversion command
    time.sleep_ms(100)  # Wait for conversion to complete
    data = i2c.readfrom(addr, 2)  # Read 2 bytes of ADC value
    adc_value = (data[0] << 8) | data[1]  # Combine bytes to get ADC value
    return adc_value

def get_adc_voltage():
    adc_value = get_adc_value()
    voltage = (adc_value * 3300) / 4096  # Convert ADC value to millivolts (assuming 3.3V reference voltage)
    return voltage

# Read and print ADC value in millivolts
while True:
    adc_voltage = get_adc_voltage()
    print("ADC Value: {} mV".format(adc_voltage))
    time.sleep(1)