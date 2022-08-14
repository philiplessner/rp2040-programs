import network
import socket
from time import sleep
from machine import Pin
from mysecrets import get_credentials


led_one = Pin(14, Pin.OUT)
led_two = Pin(15, Pin.OUT)

def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

def Website():
    value_one = led_one.value()
    value_two = led_two.value()
    website = get_html("./led.html")
    website = website.format(value_one, value_two)
    return website


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ssid, password = get_credentials()
wlan.connect(ssid, password)
    
max_wait = 10
print('Waiting for connection')
while max_wait > 10:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1    
    sleep(1)
status = None
if wlan.status() != 3:
    raise RuntimeError('Connections failed')
else:
    status = wlan.ifconfig()
    print('connection to', ssid,'succesfull established!', sep=' ')
    print('IP-adress: ' + status[0])
ipAddress = status[0]
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
# Enable the same IP address to be used after a reset so Pico W
# doesn't need full power down
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
while True:
    try:
        cl, addr = s.accept()
        print('Connection from ', addr, "accepted!")
        request = cl.recv(1024)
        request = str(request)      
        print("request is: ", request)
        if request.find('/led/one') == 6:
            led_one.toggle()
            
        if request.find('/led/two') == 6:
            led_two.toggle()
             
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(Website())
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
