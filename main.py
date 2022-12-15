from machine import Timer
import time
import gc
from machine import Pin
from machine import ADC
from machine import UART
import neopixel

#globals
externalLED = Pin(0, Pin.OUT)
internalLED = Pin("LED", Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(4), 8)
uart1 = UART(1, baudrate=9600)
uart1.init(9600, bits=8, parity=None, stop=1) # init with given parameters
t = Timer()

def toggleLEDs():
    externalLED.toggle()
    internalLED.toggle()

def writeUART(message):
    uart1.write(message)  # write 5 bytes
    
def mainLoop(timer):
    writeUART("Test UART")
    toggleLEDs()
    
t.init(freq=5000, mode=Timer.PERIODIC, callback=mainLoop)
