from machine import Timer
import settingsService 
import time
import gc
from machine import ADC
import logger
import network
from machine import Pin

wlan = network.WLAN(network.STA_IF)

def connect():
    internalLED = Pin("LED", Pin.OUT)
    internalLED.on()
    logger.info("WiFi: Connecting")
    ssid = settingsService.get('ssid')
    pw = settingsService.get('pw')
    wlan.active(True)
    wlan.scan()
    wlan.connect(ssid, pw)
    internalLED.off()
    time.sleep(5)
    if wlan.isconnected():
        logger.info("WiFi: Connected")
        internalLED.on()
    else:
        logger.info("WiFi: Failed to connect")
        internalLED.off()


def isconnected():
    return wlan.isconnected()

def disconnect():
    if wlan.isconnected():
        wlan.disconnect()
    return wlan