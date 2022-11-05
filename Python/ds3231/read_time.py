import urtc
from machine import I2C, Pin
import time

i2c = I2C(1, scl=Pin(3), sda=Pin(2))
rtc = urtc.DS3231(i2c)
time.sleep_ms(200)

while True:
    datetime = rtc.datetime()
    print(f"{datetime.year}-{datetime.month}-{datetime.day} {datetime.hour}:{datetime.minute}:{datetime.second}")
    time.sleep(1)
