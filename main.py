from machine import Timer
import time
import gc
from machine import Pin
from machine import ADC
from machine import UART
import neopixel
from collections import namedtuple
from collections import OrderedDict
import network


#globals
d = OrderedDict()

d["pin0"] = Pin(0, Pin.OUT)
d["pin1"] = Pin(1, Pin.OUT)
d["pin10"] = Pin(10, Pin.OUT)
d["pin11"] = Pin(11, Pin.OUT)
d["pin12"] = Pin(12, Pin.OUT)

internalLED = Pin("LED", Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(4), 8)
uart1 = UART(1, baudrate=9600)
uart1.init(9600, bits=8, parity=None, stop=1) # init with given parameters
t = Timer()

def toggleLEDs():
    internalLED.toggle()

def writeUART(message):
    uart1.write(message)  # write 5 bytes
    
def mainLoop(timer):
    writeUART("Test UART")
    toggleLEDs()
    loopLEDs()
    
def loopLEDs():
    for key, val in d.items():
        val.toggle()
        
    
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.scan()
    # connect to a WiFi network
    wlan.connect("BOOBERFRAGGLE", "Womble123")
    # check the connection status
    if wlan.isconnected():
        print("Connected to WiFi network")
    else:
        print("Unable to connect to WiFi network")

connect()
t.init(freq=20000, mode=Timer.PERIODIC, callback=mainLoop)
