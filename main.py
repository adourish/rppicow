from machine import Timer
import settingsService 
import time
import gc
from machine import ADC
import logger
import network
import gpioService
from machine import Pin
import wifiService
import tasksService

t = Timer()

def mainLoop():
    logger.info("Main: Start main loop")
    wlan = wifiService.connect() 
    time.sleep(3)   
    gpioService.loopLEDs()
    tasksService.getTasks()
    time.sleep(5)
    wlan = wifiService.disconnect(wlan)
    logger.info("Main: End main loop")
    time.sleep(10)

#t.init(freq=20000, mode=Timer.PERIODIC, callback=mainLoop)

mainLoop()
