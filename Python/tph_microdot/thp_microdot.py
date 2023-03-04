import machine
from machine import RTC
from machine import I2C
from microdot_asyncio import Microdot
from WiFi import WiFi
import bme280
from worldtimeapi import get_local_time

app = Microdot()

def set_RTC_Time():
    # Set up the real time clock from the World Time API server
    year, month, day, hour, minute, second, dow, doy = get_local_time()
    rtc.datetime((year, month, day, dow, hour, minute, second, 0))
    print("Local Real Time Clock: {0}-{1}-{2} {4}:{5}:{6}".format(*(rtc.datetime())))
    
def get_RTC_Time():
    t = rtc.datetime()
    s = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][t[3]]
    s += " {:04}-{:02}-{:02}".format(t[0], t[1], t[2])
    s += " {:02}:{:02}:{:02}".format(t[4], t[5], t[6])
    return s
    
@app.route('/')
async def hello(request):
    current_time = get_RTC_Time()
    t, p, h = bme.read_compensated_data()
    temperature = t / 100.  #C
    pressure = p / (256. *100.) * 0.750061  #mmHg
    RH = h / 1024.
    with open('./index.html', 'r') as f:
        content = f.read()
    htmldoc = content.format(current_time, temperature, RH, pressure)
    return htmldoc, 200, {'Content-Type': 'text/html'}

@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

if __name__ == "__main__":
    wifi= WiFi()
    wifi.setup()
    ip = wifi.connect()
    wifi.macaddress()
    essid = wifi.essid()
    wifi.channel()
    wifi.txpower()
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
    bme = bme280.BME280(i2c=i2c, address=0x76)
    rtc = RTC()
    set_RTC_Time()
    app.run(debug=True)