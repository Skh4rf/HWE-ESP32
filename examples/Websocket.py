import network
from machine import Pin, I2C, UART
import time
import urequests

slave2w = 0x3e
comsend = 0x00
datasend = 0x40
line2 = 0xC0

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

# WLAN-Hotspot konfigurieren
ap = network.WLAN(network.AP_IF)
ap.config(essid="ESP-Test", password="Passwort123")
ap.active(True)
print(ap.ifconfig())

count = 0

def DisplayWrite(text):
    i2c.writeto(slave2w, bytes([datasend]) + text)

def DisplayNextLine():
    i2c.writeto(slave2w, bytes([comsend, line2]))

def DisplayInit():
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

# Webserver-Handler für LED-Steuerung
def handle_led(request):
    global count
    count += 1
    print(request)
    DisplayInit()
    DisplayWrite("Zaehlerstand:")
    DisplayNextLine()
    DisplayWrite(str(count))
    return "Erfolg!"

# Webserver starten
def start_webserver():
    import usocket as socket

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 80))
    server.listen(1)

    while True:
        client, addr = server.accept()
        request = client.recv(1024)
        request = str(request)
        if "GET /led" in request:
            response = handle_led(request)
        else:
            response = "Unbekannte Anfrage"
        response_headers = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
        client.send(response_headers + response)
        client.close()

# Hauptprogramm
def main():
    DisplayInit()
    DisplayWrite("Ready!")
    start_webserver()
    

# Programm ausführen
main()