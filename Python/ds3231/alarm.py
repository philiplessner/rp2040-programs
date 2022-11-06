import urtc
from machine import I2C, Pin
import time
from ssd1306 import SSD1306_I2C


clock_i2c = I2C(1, scl=Pin(3), sda=Pin(2))
ds = urtc.DS3231(clock_i2c)
time.sleep_ms(200)
oled_i2c=I2C(0,sda=Pin(12), scl=Pin(13), freq=400000)
oled = SSD1306_I2C(128, 32, oled_i2c)
led = Pin(6, Pin.OUT)
led.value(0)
on_time = 2 # minutes

alarm_set= urtc.datetime_tuple(hour=20, minute=27, second=0)
ds.alarm_time(datetime=alarm_set)
ds.alarm(False)
alarmtime = ds.alarm_time()
print(f"Alarm: {alarmtime}")
timer = urtc.datetime_tuple(hour=alarm_set.hour, minute=alarm_set.minute+on_time,
                            second=alarm_set.second)
gpio_off = True
gpio_on = False


while True:
    datetime = ds.datetime()
    oled.fill(0)
    oled.text(f"{datetime.year}-{datetime.month}-{datetime.day}", 0, 0)
    oled.text(f"{datetime.hour}:{datetime.minute}:{datetime.second}", 0, 8)
    oled.text(f"Alarm: {alarmtime.hour}:{alarmtime.minute}", 0, 16)
    oled.show()
    #print(f"{datetime.year}-{datetime.month}-{datetime.day} {datetime.hour}:{datetime.minute}:{datetime.second}")
    alarm_state = ds.alarm()
    print(f"Alarm State: {alarm_state}")
    if (alarm_state and gpio_off) :
        led.value(1)
        gpio_off = False
        gpio_on = True
        ds.alarm(value=False)
        ds.alarm_time(datetime=timer)
    elif (alarm_state & gpio_on):
        led.value(0)
        gpio_off = True
        gpio_on = False
        ds.alarm(value=False)
        ds.alarm_time(datetime=alarm_set)
    time.sleep(1)