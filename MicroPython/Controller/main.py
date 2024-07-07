import machine
import uos
from machine import Pin
import time
import DisplayManager
import InputManager

def GetCPUTemp():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 2)


if __name__ == '__main__':

    sck=10
    mosi=11
    miso=14 

    displayCS=8
    displayCSPin = Pin(displayCS, Pin.OUT)

    sdCS=9
    sdCSPin = Pin(sdCS, Pin.OUT)


    adcpin = 4
    sensor = machine.ADC(adcpin)


    spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=Pin(sck), mosi=Pin(mosi))
    
    
    
    inputManager = InputManager.input_manager()

    displayManager = DisplayManager.display_manager(spi, displayCSPin, inputManager)
    

    while(True):
        
        inputManager.stick1.GetAxisY()
        displayManager.Update(GetCPUTemp())
        
        inputManager.Update()
        time.sleep(.1)

    print("completed")




