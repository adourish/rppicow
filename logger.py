import ntptime
import time

def getTime():
    now = time.localtime()
    dt = "{}/{}/{}".format(now[1], now[2], now[0])
    dh = "{}:{}".format(now[3], now[4])
    t = dt + " " + dh
    return t

def init(level):
    #ntptime.settime()
    t = getTime()
    m = t + ":Init logging service"
    print(m)

def info(message):
    t = getTime()
    m = "INFO:" + t + ":" + message
    print(m)

def warn(message):
    t = getTime()
    m = "WARN:" + t + ":" + message
    print(m)

def error(message):
    t = getTime()
    m = "ERROR:" + t + ":" + message
    print(m)

def trace(message):
    t = getTime()
    m = "TRACE:" + t + ":" + message
    print(m)