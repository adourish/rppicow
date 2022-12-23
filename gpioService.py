import machine
from collections import OrderedDict
from machine import Pin
#globals
d = OrderedDict()


d["pin0"] = Pin(0, Pin.OUT)
d["pin1"] = Pin(1, Pin.OUT)
d["pin10"] = Pin(10, Pin.OUT)
d["pin11"] = Pin(11, Pin.OUT)
d["pin12"] = Pin(12, Pin.OUT)


def loopLEDs():
    for key, val in d.items():
        val.toggle()