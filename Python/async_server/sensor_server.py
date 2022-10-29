import time
import machine
from machine import RTC
from machine import I2C
from WiFi import WiFi
from async_server import AsyncHTTPServer
from ntp import set_time
import time_convert as tc
import bme280
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

      
class SensorServer(AsyncHTTPServer):
    
    def __init__(self, host="0.0.0.0", port=80, backlog=5, timeout=20):
        super().__init__(host="0.0.0.0", port=80, backlog=5, timeout=20)
        # Set up for internal temperature sensor
        # self.sensor_temp = machine.ADC(4)
        # self.conversion_factor = 3.3 / 65535
        # Set up bme280 sensor
        i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
        self.bme = bme280.BME280(i2c=i2c, address=0x76)
        

    def customize_html(self, content):
        tz = [ [         -5, 0, 0],  # Time offset  [      H,M,S] -5 US/Eastern 
           [  3, 13, 1, 0, 0],  # Start of DST [ M,D, H,M,S] Mar 13
           [ 11, 6, 2, 0, 0],  # End   of DST [ M,D, H,M,S] Nov 6
           [         1, 0, 0]  # DST Adjust   [      H,M,S] +1 hour
       ]
        utc = tc.UtcTime()
        loc = tc.LocalTime(tz)
        current_time = f"{tc.Readable(utc)}"
        print("Current Date/Time: ", current_time)
        mylcd.get_lcd().clear()
        mylcd.get_lcd().putstr(' '.join([current_time[9:14], current_time[15:20]]))
        #reading = self.sensor_temp.read_u16() * self.conversion_factor
        #temperature = 27.0 - (reading - 0.706)/0.001721
        t, p, h = self.bme.read_compensated_data()
        temperature = t / 100.
        pressure = p / (256. *100.)
        RH = h / 1024.
        mylcd.get_lcd().move_to(0, 1)
        mylcd.get_lcd().putstr("{0:.1f}{1}C {2:.0f}%RH".format(temperature, chr(223), RH))
        custom = content.format(current_time, temperature, RH, pressure)
        return custom


class LCDDisplay():
    
    def __init__(self, i2c_per=0, sda=machine.Pin(0), scl=machine.Pin(1)):
        I2C_ADDR     = 0x27
        I2C_NUM_ROWS = 2
        I2C_NUM_COLS = 16
        self.i2c_per = i2c_per
        self.sda = sda
        self.scl = scl
        lcd_i2c = I2C(self.i2c_per, sda=self.sda, scl=self.scl, freq=400000)
        self.lcd = I2cLcd(lcd_i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
        
    def get_lcd(self):
        return self.lcd


if __name__ == "__main__":
    mylcd = LCDDisplay(i2c_per=1, sda=machine.Pin(2), scl=machine.Pin(3))
    mylcd.get_lcd().clear()
    mylcd.get_lcd().putstr("Connecting to WiFi")
    wifi= WiFi()
    wifi.setup()
    ip = wifi.connect()
    mylcd.get_lcd().clear()
    mylcd.get_lcd().putstr(f"IP {ip}")
    wifi.macaddress()
    essid = wifi.essid()
    mylcd.get_lcd().move_to(0, 1)
    mylcd.get_lcd().putstr(f"SSID {essid}")
    wifi.channel()
    wifi.txpower() 
    
    sensorserver = SensorServer()
    sensorserver.run()
