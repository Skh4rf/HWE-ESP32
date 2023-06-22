from machine import Pin, I2C, UART
import time

# I2C-Adresse des Displays
slave2w = 0x3e
# Befehls- und Datercommandcode für das Display
comsend = 0x00
datasend = 0x40
# Adresse der zweiten Zeile des Displays
line2 = 0xC0

# Initialisierung der I2C-Kommunikation
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# Scan nach I2C-Geräten
devices = i2c.scan()

# Funktion zum Schreiben von Text auf das Display
def DisplayWrite(text):
    i2c.writeto(slave2w, bytes([datasend]) + text)

# Funktion zum Wechseln zur nächsten Zeile des Displays
def DisplayNextLine():
    i2c.writeto(slave2w, bytes([comsend, line2]))

# Funktion zur Initialisierung des Displays
def DisplayInit():
    i2c.writeto(slave2w, bytes([comsend, 0x38]))  # Function set: 8-bit data
    time.sleep_ms(10)
    i2c.writeto(slave2w, bytes([comsend, 0x39]))  # Function set: 8-bit data + instruction table 1
    time.sleep_ms(10)
    i2c.writeto(slave2w, bytes([comsend, 0x14]))  # Setze OSC frequency
    i2c.writeto(slave2w, bytes([comsend, 0x78]))  # Setze contrast
    i2c.writeto(slave2w, bytes([comsend, 0x5D]))  # Setze ICON display ON | Booster ON | contrast
    i2c.writeto(slave2w, bytes([comsend, 0x6D]))  # Setze follower circuit ON | Set follower ratio
    i2c.writeto(slave2w, bytes([comsend, 0x0C]))  # Setze display ON
    i2c.writeto(slave2w, bytes([comsend, 0x01]))  # Clear display
    i2c.writeto(slave2w, bytes([comsend, 0x06]))  # Entry mode | Increment
    time.sleep_ms(10)

# Überprüfen, ob die Display-Adresse in den gefundenen Geräten vorhanden ist
if 62 in devices:
    print("Display-Address found!")
    DisplayInit()
    DisplayWrite("Ready!")     
else:
    print("Display-Address NOT found!")
    
time.sleep(3)

# Schleife zur kontinuierlichen Aktualisierung des Displays
while True:
    DisplayInit()
    DisplayWrite("   Username:    ")
    DisplayNextLine()
    DisplayWrite("      XXX       ")
    time.sleep(1)
    DisplayInit()
    DisplayWrite("   Password:    ")
    DisplayNextLine()
    DisplayWrite("      XXX       ")
    time.sleep(1)