import machine
import bme280 # from bme280.py
import utime

i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16))
bme = bme280.BME280(i2c=i2c, address=0x76)

while True:
    t, p, h = bme.read_compensated_data()
    temperature = t / 100.
    pressure = p / (256. *100.)
    RH = h / 1024.
    print("{:.2f} C\t{:.2f} hPa\t{:.1f}%".format(temperature, pressure, RH))
    #print(bme.values[0])
    utime.sleep(0.5)