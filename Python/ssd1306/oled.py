from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 32, i2c)

while True:
    oled.fill(0)
    oled.text("WELCOME!", 0, 0)
    oled.text("This is a text", 0, 8)
    oled.text("GOOD BYE", 0, 16)
    oled.show()
