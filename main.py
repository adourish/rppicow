from machine import Timer
import time
import gc
import network
from machine import SPI
import framebuf
import utime
import urequests as requests
import json
import gc
from machine import ADC
from machine import Pin
import ntptime
import time
t = Timer()
import uos
from ucryptolib import aes
import config
import ntptime



class LoggerService():
    def __init__(self, levels, timeUrl, ntptime):
        self.levels = levels
        self.timeUrl = timeUrl
   

    def setTime(self):

        ntptime.settime()
        self.trace("Logger: set time:" + self.getDateTime())
        

    def getTime(self):
        now = time.localtime()
        dh = "{}:{}".format(now[3], now[4])
        t =  dh
        return t
        
    def getDateTime(self):
        now = time.localtime()
        dt = "{}/{}/{}".format(now[1], now[2], now[0])
        dh = "{}:{}".format(now[3], now[4])
        t = dt + " " + dh
        return t

    def info(self, message):
        s = self.getDateTime()
        m = "INFO:" + s  + ":" + message
        print(m)

    def warn(self, message):
        s = self.getDateTime()
        m = "WARN:" + ":" + message
        print(m)

    def error(self, message):
        s = self.getDateTime()
        m = "ERROR:" + s  + ":" + message
        print(m)

    def trace(self, message):
        s = self.getDateTime()
        m = "TRACE:" + s  + ":" + message
        print(m)

    def debug(self, message):
        s = self.getDateTime()
        m = "DEBUG:" + s  + ":" + message
        #print(m)
    
class EncrptionService():
    def __init__(self, cipherkey, loggerService):
        self.cipherkey = cipherkey
        self.MODE_ECB = 1
        self.MODE_CBC = 2
        self.MODE_CTR = 6
        self.BLOCK_SIZE = 16
        self.loggerService = loggerService

    def encrypt(self, plaintext):
        cipher = aes(self.cipherkey, self.MODE_ECB)
        pad = self.BLOCK_SIZE - len(plaintext) % self.BLOCK_SIZE
        plaintext = plaintext + " "*pad
        encrypted = cipher.encrypt(plaintext)
        print('AES-ECB encrypted:', encrypted )
        return encrypted

    def decrypt(self, encrypted):
        cipher = aes(self.cipherkey,1) # cipher has to renew for decrypt 
        decrypted = cipher.decrypt(encrypted)
        print('AES-ECB plaintext:', decrypted)
        return decrypted

class EpaperService():
    def __init__(self, epd, loggerService):
        self.epd = epd
        self.loggerService = loggerService
        
        self.rowHeight = 15
        self.x = 0
        self.y = 0
        self.xmax = 16
        self.xmax1 = self.xmax + 1
        self.xmax2 = 32
        self.xmax3 = 32 + 1
        self.row = 1
        self.maxrows = 16

    def clear(self):
        self.epd.Clear(0xff)
        self.epd.fill(0xff)

    def nl(self):
        self.y = self.y + self.rowHeight
        self.row = self.row +1

    def drawnl(self):
        self.y = self.y + 7
        self.epd.hline(0, self.y + 2, 140, 0x00)
        self.y = self.y + 5

    def draw(self):
        self.epd.display(epd.buffer)
        self.epd.delay_ms(2000)

    def writeDate(self):
        dt = self.loggerService.getTime()
        self.epd.text(dt, self.x, self.y, 0x00)
        self.loggerService.trace("ePaper:writedate:" +dt)
        self.drawnl()
        

    def writeTask(self, duedt, content, label, row):
        if self.row <= self.maxrows:
            if len(content) <= self.xmax:
                r1 = content
                r2 = None
                r3 = None
            elif len(content) > self.xmax and len(content) <= self.xmax2:
                r1 = content[0:self.xmax]
                r2 = content[self.xmax:len(content)]
                r3 = None
            elif len(content) > self.xmax:
                r1 = content[0:self.xmax]
                r2 = content[self.xmax1:self.xmax2]
                r3 = content[self.xmax2:len(content)]
            r4 = "[" + duedt + "][" + label +"]"   

            self.epd.text(r1, self.x, self.y, 0x00)
            self.loggerService.trace("ePaper:x" + ":" + str(self.x) + "-y:" + str(self.y) + "-" + r1)
            if r2 is not None:
                self.nl()
                self.epd.text(r2, self.x, self.y, 0x00)
                self.loggerService.trace("ePaper:x" + ":" + str(self.x) + "-y:" + str(self.y) + "-" + r2)
            if r3 is not None:
                self.nl()
                self.epd.text(r3, self.x, self.y, 0x00)
                self.loggerService.trace("ePaper:x" + ":" + str(self.x) + "-y:" + str(self.y) + "-" + r3)
            
            self.nl()
            self.epd.text(r4, self.x, self.y, 0x00)
            self.loggerService.trace("ePaper:x" + ":" + str(self.x) + "-y:" + str(self.y) + "-" + r4)
            self.drawnl()
          


class TasksService():
    def __init__(self, settingsService, loggerService, epaperService):
        self.settingsService = settingsService
        self.loggerService = loggerService
        self.token = settingsService.get("token")
        self.tasksUrl = settingsService.get("tasksUrl")
        self.epaperService = epaperService
        
    def getTasks(self):
        

        header_data = { 
            "content-type": 'application/json; charset=utf-8', 
            "Authorization": self.token,
            "devicetype": '1'
            }
        header_data["token"] = self.token
        res = requests.get(self.tasksUrl, headers = header_data)
        text = res.text
        self.loggerService.debug("Tasks:" + text)
        r = json.loads(text)
        for item in r:
            section = ""
            list = item["labels"]
            content = item["content"]
            section_id = item["section_id"]
            project_id = item["project_id"]
            if section_id == "110614030":
                section = "Todo"
            if section_id == "110614081":
                section = "Recur"
            if section_id == "110613672":
                section = "Active"
            if section_id == "":
                section = "Backlog"

            labels = ""
            for label in list:
                if labels == "":
                    labels = labels + "" + label
                else:
                    labels = labels + "," + label

            if item["due"] is None:
                duedt = "N/A"
            else:
                _duedt = item["due"]["date"]
                duedt = _duedt[5:10]
            item["duedt"] = duedt
            m = section + "-" + content
            item["section"] = section
            item["label"] = labels
            self.loggerService.debug("Task:" + m)

        return r

    def getItemText(self, item):
        due = ""
        list = item["labels"]
        content = item["content"]
        section_id = item["section_id"]
        project_id = item["project_id"]
        section = item["section"]
        duedt = item["duedt"]
        label = item["label"]

        m = "(" + duedt + ")" + section + "-" + content + " [" + label + "]"
        return m

    def displayHeader(self):
        self.epaperService.clear()
        self.epaperService.writeDate()

    def displayFooter(self):
        self.epaperService.draw()

    def displayTasks(self, items, displaySection):  
        i = 1
        for item in items:
            m = self.getItemText(item)
            content = item["content"]
            section_id = item["section_id"]
            project_id = item["project_id"]
            section = item["section"]
            duedt = item["duedt"]
            label = item["label"]
            if section == displaySection:
                if self.epaperService is None:
                    self.loggerService.trace("no E-paper:" + displaySection +":" + m)
                else:
                    self.loggerService.trace("E-paper:" + displaySection +":" + m)
                    self.epaperService.writeTask(duedt, content, label, i)
                    i = i + 1

            

    def getFirstTask(self, val): 
        for value in val:
            self.loggerService.trae("Task:" + value["content"])
            return value

    def getTaskItem(self):
        items = self.getTasks()
        item = self.getFirstTask(items)

class StatusService():
    def __init__(self, loggerService, settingsService):
        self.statusLED1 = Pin(18, Pin.OUT)
        self.statusLED2 = Pin(19, Pin.OUT)
        self.statusLED3 = Pin(20, Pin.OUT)
        self.statusLED4 = Pin(21, Pin.OUT)

    def start(self):
        self.statusLED1.on()
        self.statusLED2.off()
        self.statusLED3.off()
        self.statusLED4.off()

    def active(self):
        self.statusLED1.off()
        self.statusLED2.on()
        self.statusLED3.off()
        self.statusLED4.off()
        
    def done(self):
        self.statusLED1.off()
        self.statusLED2.off()
        self.statusLED3.on()
        self.statusLED4.off()
    
    def error(self):
        self.statusLED1.off()
        self.statusLED2.off()
        self.statusLED3.off()
        self.statusLED4.on()

class WifiService():
    def __init__(self, loggerService, settingsService):
        self.loggerService = loggerService
        self.settingsService = settingsService
        self.wlan = network.WLAN(network.STA_IF)
        self.internalLED = Pin("LED", Pin.OUT)

    def connect(self):
        
        self.loggerService.info("WiFi: Connecting")
        ssid = self.settingsService.get('ssid')
        pw = self.settingsService.get('pw')
        if self.wlan.isconnected():
            self.loggerService.info("WiFi: Already Connected")
        else:
            self.wlan.active(True)
            self.wlan.scan()
            self.wlan.connect(ssid, pw)
        
        time.sleep(2)
        if self.wlan.isconnected():
            self.loggerService.info("WiFi: Connected")
            self.internalLED.on()
        else:
            self.loggerService.error("WiFi: Failed to connect")
            self.internalLED.off()


    def isconnected(self):
        return self.wlan.isconnected()

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
        self.internalLED.off()
        return self.wlan


class SettingsService():
    def __init__(self, s, loggerService):
        self.s = s
        self.loggerService = loggerService

    def get(self, key):
        s = self.s[key]
        m = "get key=" + key + " " + s
        self.loggerService.debug(m)
        return s
    

class App():
    def __init__(self, loggerService, settingsService, wifiService, tasksService, encrptionService, statusService):
        self.loggerService = loggerService
        self.settingsService = settingsService
        self.wifiService = wifiService
        self.tasksService = tasksService
        self.encrptionService = encrptionService
        self.statusService = statusService
        self.statusService.start()
        
    def main(self):
        try:
            self.statusService.active()
            self.loggerService.trace("Main: Start main loop")
            wlan = self.wifiService.connect() 
            self.loggerService.setTime()
            items = self.tasksService.getTasks()
            self.tasksService.displayHeader()
            self.tasksService.displayTasks(items, "Todo")
            self.tasksService.displayTasks(items, "Active")
            self.tasksService.displayFooter()
            wlan = self.wifiService.disconnect()
            self.loggerService.trace("Main: End main loop")
            self.statusService.done()
        except OSError:
            self.statusService.error()
            self.loggerService.error("Main: Error")

########################################################################################
# Display resolution
# Display resolution
EPD_WIDTH       = 128
EPD_HEIGHT      = 296

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

WF_PARTIAL_2IN9 = [
    0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0A,0x0,0x0,0x0,0x0,0x0,0x1,  
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x1,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x0,0x0,0x0,0x0,0x0,0x0,0x0,
    0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,
    0x22,0x17,0x41,0xB0,0x32,0x36,
]

class EPD_2in9(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.lut = WF_PARTIAL_2IN9
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50) 
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)   

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 1):      #  0: idle, 1: busy
            self.delay_ms(10) 
        print("e-Paper busy release")  

    def TurnOnDisplay(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0xF7)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.ReadBusy()

    def TurnOnDisplay_Partial(self):
        self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
        self.send_data(0x0F)
        self.send_command(0x20) # MASTER_ACTIVATION
        self.ReadBusy()

    def SendLut(self):
        self.send_command(0x32)
        for i in range(0, 153):
            self.send_data(self.lut[i])
        self.ReadBusy()

    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start>>3) & 0xFF)
        self.send_data((x_end>>3) & 0xFF)
        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(x & 0xFF)
        
        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
        self.ReadBusy()
        
    def init(self):
        # EPD hardware init start     
        self.reset()

        self.ReadBusy()   
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0x27)
        self.send_data(0x01)
        self.send_data(0x00)
    
        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width-1, self.height-1)

        self.send_command(0x21) #  Display update control
        self.send_data(0x00)
        self.send_data(0x80)	
    
        self.SetCursor(0, 0)
        self.ReadBusy()
        # EPD hardware init end
        return 0

    def display(self, image):
        if (image == None):
            return            
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
        self.TurnOnDisplay()

    def display_Base(self, image):
        if (image == None):
            return   
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])
                
        self.send_command(0x26) # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
                
        self.TurnOnDisplay()
        
    def display_Partial(self, image):
        if (image == None):
            return
            
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(2)   
        
        self.SendLut()
        self.send_command(0x37) 
        self.send_data(0x00)  
        self.send_data(0x00)  
        self.send_data(0x00)  
        self.send_data(0x00) 
        self.send_data(0x00)  	
        self.send_data(0x40)  
        self.send_data(0x00)  
        self.send_data(0x00)   
        self.send_data(0x00)  
        self.send_data(0x00)

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x22) 
        self.send_data(0xC0)   
        self.send_command(0x20) 
        self.ReadBusy()

        self.SetWindow(0, 0, self.width - 1, self.height - 1)
        self.SetCursor(0, 0)
        
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])
        self.TurnOnDisplay_Partial()

    def Clear(self, color):
        self.send_command(0x24) # WRITE_RAM
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(color)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE
        self.send_data(0x01)
        
        self.delay_ms(2000)
        self.module_exit()
########################################################################################


if __name__=='__main__':
    epd = EPD_2in9()
    i = 0
    while i == 0:
        
        _settings = config.settings
        _cipherkey = config.cipherkey
        _levels = config.levels
        _timeUrl = _settings["timeUrl"]
        _loopIntervalS = _settings["loopIntervalS"]
        
        l = LoggerService(_levels, _timeUrl, ntptime)
        e = EpaperService(epd, l)
        c = EncrptionService(_cipherkey, l)
        s = SettingsService(_settings, l)
        t = TasksService(s, l, e)
        ws = WifiService(l, s)
        st = StatusService(l, s)
        l.info("MainLoop:"  + ":Start loop")
        l.info("Main: Interval Seconds:" + str(_loopIntervalS))
        app = App(l, s, ws, t, c, st)
        app.main()
        l.info("MainLoop:" + ":End loop")
        time.sleep(60)



