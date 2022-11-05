import urtc
from machine import I2C, Pin
import time

i2c = I2C(1, scl=Pin(3), sda=Pin(2))
rtc = urtc.DS3231(i2c)
time.sleep_ms(200)

datetime = urtc.datetime_tuple(year=2022, month=11, day=4,
                               weekday=4, hour=20, minute=47, second=0)
rtc.datetime(datetime)

datetime = rtc.datetime()
print(datetime.year)
print(datetime.month)
print(datetime.day)
print(datetime.weekday)
print(datetime.hour)
print(datetime.minute)
print(datetime.second)