from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import urtc
import time


oled_i2c=I2C(0,sda=Pin(12), scl=Pin(13), freq=400000)
oled = SSD1306_I2C(128, 32, oled_i2c)
clock_i2c = I2C(1, scl=Pin(3), sda=Pin(2))
rtc = urtc.DS3231(clock_i2c)
time.sleep_ms(200)

while True:
    datetime = rtc.datetime()
    print(f"{datetime.year}-{datetime.month}-{datetime.day} {datetime.hour}:{datetime.minute}:{datetime.second}")
    oled.fill(0)
    oled.text(f"{datetime.year}-{datetime.month}-{datetime.day}", 0, 0)
    oled.text(f"{datetime.hour}:{datetime.minute}:{datetime.second}", 0, 8)
    oled.show()
    time.sleep(1)
