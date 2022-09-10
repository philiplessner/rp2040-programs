import time
import machine
from machine import RTC
from WiFi import WiFi
from async_server import AsyncHTTPServer
from ntp import set_time

      
class TimeServer(AsyncHTTPServer):

    def customize_html(self, content):
        UTC_OFFSET = -4 * 60 * 60
        dt = time.localtime(time.time() + UTC_OFFSET)
        date = '-'.join([str(dt[0]), str(dt[1]), str(dt[2])])
        local_time = ':'.join([str(dt[3]), str(dt[4]), str(dt[5])])
        current_time = date + "  " + local_time
        print("Current Date/Time: ", current_time)
        custom = content.format(current_time)
        return custom


if __name__ == "__main__":
    wifi= WiFi()
    wifi.setup()
    wifi.connect()
    wifi.info()
    
    rtc = RTC()
    set_time()
    print("Real Time Clock: ", rtc.datetime())
    
    timeserver = TimeServer()
    timeserver.run()
