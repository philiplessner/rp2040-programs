import urtc
from machine import I2C, Pin
import utime as time
i2c = I2C(1, scl=Pin(3), sda=Pin(2))
rtc = urtc.DS3231(i2c)
time.sleep_ms(200) #  Need to put this delay in
datetime = urtc.datetime_tuple(year=2016, month=8, day=14)
rtc.datetime(datetime)

datetime = rtc.datetime()
print(datetime.year)
print(datetime.month)
print(datetime.day)
print(datetime.weekday)