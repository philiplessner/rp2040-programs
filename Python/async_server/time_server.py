import time
import network
import ubinascii
import machine
from machine import RTC
from mysecrets import get_credentials
from async_server import AsyncHTTPServer

rtc = RTC()
rtc.datetime((2022, 9, 5, 2, 13, 40, 0, 0))
print("Initial Time:", rtc.datetime())
      
class TimeServer(AsyncHTTPServer):

    def customize_html(self, content):
        #current_time = time.ctime()
        dt = rtc.datetime()
        date = '-'.join([str(dt[0]), str(dt[1]), str(dt[2])])
        time = ':'.join([str(dt[4]), str(dt[5]), str(dt[6])])
        current_time = date + "  " + time
        print("Current Time: ", current_time)
        custom = content.format(current_time)
        return custom


# Set country to avoid possible errors
rp2.country('US')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# If you need to disable powersaving mode
# wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))

# Load login data from different file for safety reasons
ssid, pw = get_credentials()
wlan.connect(ssid, pw)
from mysecrets import get_credentials
# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth
if wlan.status() != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(wlan.status()):
        led.on()
        time.sleep(0.2)
        led.off()
        time.sleep(0.2)
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])


timeserver = TimeServer()
timeserver.run()
