import neopixel
from board import *

RED = 0x100000 # (0x10, 0, 0) also works

pixels = neopixel.NeoPixel(NEOPIXEL, 6)
for i in range(len(pixels)):
    pixels[i] = RED
