import time
import machine
from machine import RTC
from WiFi import WiFi
from async_server import AsyncHTTPServer
from ntp import set_time
import time_convert as tc

      
class TimeServer(AsyncHTTPServer):
    
    def __init__(self, host="0.0.0.0", port=80, backlog=5, timeout=20):
        super().__init__(host="0.0.0.0", port=80, backlog=5, timeout=20)
        # Set up for internal temperature sensor
        self.sensor_temp = machine.ADC(4)
        self.conversion_factor = 3.3 / 65535
        

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
        reading = self.sensor_temp.read_u16() * self.conversion_factor
        temperature = 27.0 - (reading - 0.706)/0.001721
        custom = content.format(current_time, temperature)
        return custom


if __name__ == "__main__":
    wifi= WiFi()
    wifi.setup()
    wifi.connect()
    wifi.macaddress()
    wifi.essid()
    wifi.channel()
    wifi.txpower() 
    
    timeserver = TimeServer()
    timeserver.run()
