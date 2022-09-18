import network
import ubinascii
import time
from mysecrets import get_credentials


class WiFi():

    def __init__(self, type=network.STA_IF,
                 country='US', power_save=False):
        self.type = type
        self.country = country
        self.power_save = power_save

    def setup(self):
        self.wlan = network.WLAN(self.type)
        self.wlan.active(True)
        if not self.power_save:
            # If you need to disable powersaving mode
            self.wlan.config(pm=0xa11140)

    def connect(self):
        # Load login data from different file for safety reasons
        ssid, pw = get_credentials()
        self.wlan.connect(ssid, pw)
        # Wait for connection with 10 second timeout
        timeout = 10
        while timeout > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
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
        if self.wlan.status() != 3:
            raise RuntimeError('Wi-Fi connection failed')
        else:
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])

    def macaddress(self):
        # See the MAC address in the wireless chip OTP
        mac = ubinascii.hexlify(network.WLAN().config('mac'), ':').decode()
        print('mac = ' + mac)

    def essid(self):
        print(self.wlan.config('essid'))

    def channel(self):
        print(self.wlan.config('channel'))

    def txpower(self):
        print(self.wlan.config('txpower'))

