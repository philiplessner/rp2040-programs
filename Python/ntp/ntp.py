import network
import socket
import time
import struct
import machine

NTP_DELTA = 2208988800
host = "pool.ntp.org"


def set_time():
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    except OSError as exc:
        if exc.args[0] == 110: #ETIMEDOUT
            time.sleep(2)
            pass
    finally:
        s.close()
    val = struct.unpack("!I", msg[40:44])[0]
    t = val - NTP_DELTA    
    tm = time.gmtime(t)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))

if __name__ == '__main__':
    from mysecrets import get_credentials


    led = machine.Pin("LED", machine.Pin.OUT)

    ssid = 'A NETWORK'
    password = 'A PASSWORD'
    ssid, password = get_credentials()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )

    led.on()
    set_time()
    UTC_OFFSET = -4 * 60 * 60
    print('RTC Time: ', machine.RTC().datetime())
    print('UTC Time: ', time.gmtime())
    print('Local Time: ', time.localtime(time.time() + UTC_OFFSET))
    led.off()
