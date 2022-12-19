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
import urequests
from PIL import Image
import textwrap
import network
import socket

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
        
def getASCII(url):
# download the image from a URL
response = urequests.get("https://static.wikia.nocookie.net/wombles/images/c/c5/Great_uncle_bulgaria_1990s.jpg")

# open the image using the PIL library
im = Image.open(response.raw)

# resize the image to a smaller size
im = im.resize((80, 40), resample=Image.BICUBIC)

# convert the image to grayscale
im = im.convert("L")

# create a list of ASCII characters to use for the conversion
chars = "$@B%8WM#*oahkbdpwmZO0QlJYXzcvnxrjft/\|()1{}[]-_+~<>i!lI;:,"

# iterate over the pixels in the image
for y in range(im.size[1]):
    # create a list of ASCII characters for this row
    row = []
    for x in range(im.size[0]):
        # get the pixel value (0-255)
        pixel = im.getpixel((x, y))
        # map the pixel value to an ASCII character
        char = chars[int(pixel / 256 * len(chars))]
        row.append(char)
    # print the row of ASCII characters
    print("".join(row))



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
