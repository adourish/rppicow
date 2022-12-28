import epaper2in9
from machine import Pin, SPI

# SPIV on ESP32
sck = Pin(18)
miso = Pin(19)
mosi = Pin(23)
dc = Pin(32)
cs = Pin(33)
rst = Pin(19)
busy = Pin(35)
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
e = epaper4in2.EPD(spi, cs, dc, rst, busy)
e.init()
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