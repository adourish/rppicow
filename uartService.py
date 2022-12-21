
from machine import UART

uart1 = UART(1, baudrate=9600)
uart1.init(9600, bits=8, parity=None, stop=1) # init with given parameters

def writeUART(message):
    uart1.write(message)  # write 5 bytes