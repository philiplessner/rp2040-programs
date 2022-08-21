import network
import urequests
from mysecrets import get_credentials


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid, password = get_credentials()
wlan.connect(ssid, password)

# Make GET Request
r = urequests.get('http://www.google.com')
print(r.content)
r.close()
