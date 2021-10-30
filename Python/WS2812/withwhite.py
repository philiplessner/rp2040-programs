# Example using PIO to drive a set of WS2812 LEDs.

import array, time
from machine import Pin
import rp2

# Configure the number of WS2812 LEDs.
NUM_LEDS = 16
PIN_NUM = 6
brightness = 0.01

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=32) # changed

def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        gg = int(((c >> 24) & 0xFF) * brightness) #susposidly white added
        dimmer_ar[i] = (gg<<24) + (g<<16) + (r<<8) + b # ^
    sm.put(dimmer_ar, 0) # do not discard any bits
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[3]<<24)+ (color[1]<<16) + (color[0]<<8) + color[2] #needs reordering, color[3] supposed to be white


def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        time.sleep(wait)
        pixels_show()
    time.sleep(0.2)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait): #needs remaking to support the white argument
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)
        

#colors set in RGBW format 
BLACK = (0, 0, 0,0)
RED = (255, 0, 0,0)
YELLOW = (255, 150, 0,0)
GREEN = (0, 255, 0,0)
CYAN = (0, 255, 255,0)
BLUE = (0, 0, 255,0)
PURPLE = (180, 0, 255,0)
WHITE = (0,0,0,255)
ORANGE = (255,165,0,0) # added
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE, ORANGE)



pixels_fill(BLACK)
pixels_show()
time.sleep(1)
#pixels_fill(ORANGE)
#pixels_show()
pixels_set(3,RED)
#pixels_set(1,RED)
#pixels_set(3,BLUE)


pixels_show()
           
#test to find the order of color values, currently displays as BRWG
#BRWG
while 0:
    color = 255,0,0,0
    pixels_fill(color)
    pixels_show()
    time.sleep(1)
    color = 0,255,0,0
    pixels_fill(color)
    pixels_show()
    time.sleep(1)
    color = 0,0,255,0
    pixels_fill(color)
    pixels_show()
    time.sleep(1)
    color = 0,0,0,255
    pixels_fill(color)
    pixels_show()
    time.sleep(1)

#demo with rainbow disabled
while 1:
    print("color test")
    color = 0,255,0,255
    pixels_fill(color)
    pixels_show()
    time.sleep(1)
  
    print("fills")
    for color in COLORS:
        pixels_fill(color)
        pixels_show()
        time.sleep(0.1)

    print("chases")
    for color in COLORS:
        color_chase(color, 0.01)

    print("rainbow")
 #   rainbow_cycle(0)