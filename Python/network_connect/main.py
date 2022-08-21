import time
import network
import ubinascii
from mysecrets import get_credentials


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid, password = get_credentials()
wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
    print('MAC Address = ', mac)
    print('Channel = ', wlan.config('channel'))
    print('SSID = ', wlan.config('essid'))
    print('TXPower = ', wlan.config('txpower'))
