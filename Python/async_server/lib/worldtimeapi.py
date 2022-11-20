import urequests as requests
import time


def get_local_time():
    request = requests.get("http://worldtimeapi.org/api/ip")
    unixtime = int(request.json()['unixtime'])
    utc_offset = request.json()['utc_offset']
    utc_offset_numeric = int(utc_offset[0:3])
    #  (year, month, day, hour, minute, second, dow, doy)
    timestamp = time.localtime(unixtime + utc_offset_numeric*60*60)
    print(timestamp)
    return timestamp


if __name__ == '__main__':
    get_local_time()
    