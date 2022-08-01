import network
import urequests

ssid = "ATT5Mwb2RC"
password = "8ieu2x4gd7ae"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Make GET Request
r = urequests.get('http://www.google.com')
print(r.content)
r.close()