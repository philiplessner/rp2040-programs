import machine
from machine import RTC
from machine import I2C
from microdot_asyncio import Microdot
import logging
from WiFi import WiFi
import bme280
from worldtimeapi import get_local_time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


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
    print(f"{request.client_addr[0]} {request.method} from {request.headers['Host']}{request.path}")
    logger.info(f"{request.client_addr[0]} {request.method} from {request.headers['Host']}{request.path}")
    current_time = get_RTC_Time()
    t, p, h = bme.read_compensated_data()
    temperature = t / 100.  #C
    pressure = p / (256. *100.) * 0.750061  #mmHg
    RH = h / 1024.
    with open('./index.html', 'r') as f:
        content = f.read()
    htmldoc = content.format(current_time, temperature, RH, pressure)
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/log')
async def log(request):
    print(f"{request.client_addr[0]} {request.method} from {request.headers['Host']}{request.path}")
    logger.info(f"{request.client_addr[0]} {request.method} from {request.headers['Host']}{request.path}")
    filename = './server.log'
    content = ''
    with open(filename, 'r') as f:
        raws = f.readlines()[-25:]
    content = '<br>'.join([raw.strip() for raw in raws])
    prefix = '''
                <!DOCTYPE html>
                <html lang='en'> 
                <head>
                <meta charset='utf-8'>
                <title>Async</title>
                </head>
                <body>
                <div>
                <h1>Last N Lines of Log (Max: 25)</h1>
             '''
    suffix = '''
                </div>
                </body>
                </html>
             '''
    htmldoc = prefix + content + suffix
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    logger.info("Server Shutting Down")
    request.app.shutdown()
    return 'The server is shutting down...'


if __name__ == "__main__":
    # Set up logging
    logger = logging.getLogger("Server")
    fmt = "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
    logging.basicConfig(level=logging.INFO,
                        filename="server.log",
                        format=fmt)
    # Initialize LCD display
    lcd_i2c = I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=400000)
    I2C_ADDR     = 0x27
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
    lcd = I2cLcd(lcd_i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
    # Connect to WiFi and display the server address on the LCD screen
    lcd.clear()
    lcd.putstr("Connecting to WiFi")
    wifi= WiFi()
    wifi.setup()
    ip = wifi.connect()
    lcd.clear()
    lcd.putstr(f"IP {ip}")
    wifi.macaddress()
    essid = wifi.essid()
    lcd.move_to(0, 1)
    lcd.putstr(f"SSID {essid}")
    wifi.channel()
    wifi.txpower()
    # Initialize the BME280 sensor
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
    bme = bme280.BME280(i2c=i2c, address=0x76)
    # Get the time from the network
    rtc = RTC()
    set_RTC_Time()
    # Start the webserver
    host = '0.0.0.0'
    port = 80
    logger.info(f"Starting Async Server on interface {host}:{port}")
    app.run(host=host, port=port, debug=True)