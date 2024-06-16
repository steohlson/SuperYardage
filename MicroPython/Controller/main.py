import machine
import uos
from machine import Pin

#Use firmware from this repository to use driver
#https://github.com/russhughes/st7789_mpy
import st7789



sck=10
mosi=11
miso=8 #not used
res=12
dc=13
width=170
height=320



print(uos.uname())


spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=Pin(sck), mosi=Pin(mosi))
display = st7789.ST7789(spi=spi, width=width, height=height, reset=machine.Pin(res, machine.Pin.OUT), dc=machine.Pin(dc, machine.Pin.OUT), rotation=45)
display.init()


#display.fill(st7789.RED)
display.jpg("ControllerLoadingScreen.jpg", 0, 0, st7789.SLOW)
print("completed")


