from machine import Timer
import time
import gc
import network
import epaper2in9

import urequests as requests
import json
import gc
from machine import ADC
from machine import Pin
import ntptime
import time
t = Timer()

class LoggerService():
    def info(self, message):
        m = "INFO:"  + ":" + message
        print(m)

    def warn(self, message):
        m = "WARN:" + ":" + message
        print(m)

    def error(self, message):
        m = "ERROR:" + ":" + message
        print(m)

    def trace(self, message):
        m = "TRACE:" + ":" + message
        print(m)
    

class EpaperService():
    def __init__(self):
        self.epd = EPD_2in9_Landscape()
        
    def write(self, text, row):
        rowHeight = 30
        loc = rowHeight * row
        
        epd.Clear(0xff)
    
        epd.fill(0xff)
        epd.text(text, 5, 10, 0x00)

class TasksService():
    def __init__(self, settingsService, loggerService):
        self.settingsService = settingsService
        self.loggerService = loggerService
        self.token = settingsService.get("token")
        self.tasksUrl = settingsService.get("tasksUrl")

    def getTasks(self):
        header_data = { 
            "content-type": 'application/json; charset=utf-8', 
            "Authorization": self.token,
            "devicetype": '1'
            }
        header_data["token"] = self.token
        res = requests.get(self.tasksUrl, headers = header_data)
        text = res.text
        self.loggerService.info("Tasks:" + text)
        r = json.loads(text)
        return r

    def displayTasks(self):
  
        items = getTasks()
        for item in items:
            self.loggerService.info("Task:" + item["title"])
            item.row = 1
            rowText = item["title"]
            #epaperService.write(rowText, 1)

    def getFirstTask(self, val): 
        for value in val:
            self.loggerService.info("Task:" + value["content"])
            return value

    def getTaskItem(self):
        items = self.getTasks()
        item = self.getFirstTask(items)

class WifiService():
    def __init__(self, loggerService, settingsService):
        self.loggerService = loggerService
        self.settingsService = settingsService
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        internalLED = Pin("LED", Pin.OUT)
        internalLED.on()
        self.loggerService.info("WiFi: Connecting")
        ssid = self.settingsService.get('ssid')
        pw = self.settingsService.get('pw')
        self.wlan.active(True)
        self.wlan.scan()
        self.wlan.connect(ssid, pw)
        internalLED.off()
        time.sleep(5)
        if self.wlan.isconnected():
            self.loggerService.info("WiFi: Connected")
            internalLED.on()
        else:
            self.loggerService.info("WiFi: Failed to connect")
            internalLED.off()


    def isconnected(self):
        return wlan.isconnected()

    def disconnect(self):
        if wlan.isconnected():
            wlan.disconnect()
        return wlan


class SettingsService():
    def __init__(self):
        self.settings = {
        'ssid': 'BOOBERFRAGGLE',
        'pw': 'Womble123',
        'subtopic' : b'led',
        'pubtopic' : b'led',
        'token': 'Bearer 62c623e2ae7407e805dabe692f8af45ad582bcfc',
        'tasksUrl': 'https://api.todoist.com/rest/v2/tasks'
        }

    def get(self, key):
        s = self.settings[key]
        print("get key=" + key + " " + s)
        return s
    

class App():
    def __init__(self, loggerService, settingsService, wifiService, tasksService):
        self.loggerService = loggerService
        self.settingsService = settingsService
        self.wifiService = wifiService
        self.tasksService = tasksService

    def main(self):
        self.loggerService.info("Main: Start main loop")
        wlan = self.wifiService.connect() 
        time.sleep(3)   
        self.tasksService.displayTasks()
        time.sleep(5)
        wlan = self.wifiService.disconnect(wlan)
        self.loggerService.info("Main: End main loop")
        time.sleep(10)


l = LoggerService()
s = SettingsService()
t = TasksService(s, l)
ws = WifiService(l, s)
app = App(l, s, ws, t)
app.main()
