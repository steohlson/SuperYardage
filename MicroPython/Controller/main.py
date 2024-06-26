import machine
import uos
from machine import Pin
import time

#Use firmware from this repository to use driver
#https://github.com/russhughes/st7789_mpy
import st7789



sck=10
mosi=11
miso=14 
res=12
dc=13
width=170
height=320

displayCS=8
displayCSPin = Pin(displayCS, Pin.OUT)

sdCS=9
sdCSPin = Pin(sdCS, Pin.OUT)






adcpin = 4
sensor = machine.ADC(adcpin)
  
def GetCPUTemp():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 2)



sdCSPin.value(1)
displayCSPin.value(0)



print(uos.uname())


spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=Pin(sck), mosi=Pin(mosi), miso=Pin(miso))
display = st7789.ST7789(spi=spi, width=width, height=height, reset=machine.Pin(res, machine.Pin.OUT), dc=machine.Pin(dc, machine.Pin.OUT), rotation=45)
display.init()



#display.fill(st7789.RED)
display.jpg("ControllerLoadingScreen.jpg", 0, 0, st7789.SLOW)

time.sleep(2)

import vga1_16x32 as font1

display.fill(st7789.BLACK)
display.text(font1,"CPU temp: ", 0, 0)
while(True): 
    sdCSPin.value(1)
    displayCSPin.value(0)

    display.text(font1, str(GetCPUTemp()) + " C", 144, 0)
    time.sleep(.1)

print("completed")


