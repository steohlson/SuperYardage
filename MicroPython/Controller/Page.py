#Use firmware from this repository to use driver
#https://github.com/russhughes/st7789_mpy
import st7789 # type: ignore

import vga1_16x32 as font1 # type: ignore

class Page:
    display : st7789.ST7789
    def __init__(self, display):
        
        self.display = display
    
    def update(self):
        pass