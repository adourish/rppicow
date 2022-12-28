import epaper2in9
from pyb import SPI

spi = SPI(3, SPI.MASTER, baudrate=2000000, polarity=0, phase=0)
cs = pyb.Pin('PB6')
dc = pyb.Pin('PB7')
rst = pyb.Pin('PB8')
busy = pyb.Pin('PB9')
e = epaper2in9.EPD(spi, cs, dc, rst, busy)
e.init()
w = 128
h = 296
x = 0
y = 0
black = 0
white = 1

def init():
    import framebuf
    buf = bytearray(128 * 296 // 8)
    fb = framebuf.FrameBuffer(buf, 128, 296, framebuf.MONO_HLSB)
    fb.fill(white)

def write(text, row):
    rowHeight = 30
    loc = rowHeight * row
    fb.text(text,30,0,black)

def clear():
    e.clear_frame_memory(b'\xFF')
    e.display_frame()