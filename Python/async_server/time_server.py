import time
import machine
from machine import RTC
from WiFi import WiFi
from async_server import AsyncHTTPServer
from ntp import set_time
import time_convert as tc

      
class TimeServer(AsyncHTTPServer):

    def customize_html(self, content):
        tz = [ [         -5, 0, 0],  # Time offset  [      H,M,S] -5 US/Eastern 
           [  3, 13, 1, 0, 0],  # Start of DST [ M,D, H,M,S] Mar 13
           [ 11, 6, 2, 0, 0],  # End   of DST [ M,D, H,M,S] Nov 6
           [         1, 0, 0]  # DST Adjust   [      H,M,S] +1 hour
       ]
        utc = tc.UtcTime()
        #UTC_OFFSET = -4 * 60 * 60
        #dt = time.localtime(time.time() + UTC_OFFSET)
        #date = '-'.join([str(dt[0]), str(dt[1]), str(dt[2])])
        #local_time = ':'.join([str(dt[3]), str(dt[4]), str(dt[5])])
        #current_time = date + "  " + local_time
        loc = tc.LocalTime(tz)
        current_time = f"{tc.Readable(loc)}"
        #current_time = f"{tc.Readable(utc)}"
        print("Current Date/Time: ", current_time)
        custom = content.format(current_time)
        return custom


if __name__ == "__main__":
    wifi= WiFi()
    wifi.setup()
    wifi.connect()
    wifi.macaddress()
    wifi.essid()
    wifi.channel()
    wifi.txpower()
    
    rtc = RTC()
    set_time()
    print("Real Time Clock: ", rtc.datetime())
    
    timeserver = TimeServer()
    timeserver.run()
