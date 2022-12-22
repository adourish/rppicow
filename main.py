from machine import Timer
import settingsService 
import time
import gc
from machine import ADC
import logger
import neopixel
import network
import urequests
import network
import socket
import gpioService
from machine import Pin
import mqttService


np = neopixel.NeoPixel(machine.Pin(4), 8)
internalLED = Pin("LED", Pin.OUT)
t = Timer()




    
def mainLoop(timer):
    logger.info("Start main loop")
    gpioService.loopLEDs()
    mqttService.init()
    time.sleep(5)
    logger.info("End main loop")

        

def connect():
    ssid = settingsService.get('ssid')
    pw = settingsService.get('pw')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.scan()
    wlan.connect(ssid, pw)
    time.sleep(5)
    if wlan.isconnected():
        logger.info("Connected to WiFi network")
        internalLED.on()
    else:
        logger.info("Unable to connect to WiFi network")
        internalLED.off()

logger.init("INFO")
connect()


t.init(freq=20000, mode=Timer.PERIODIC, callback=mainLoop)
