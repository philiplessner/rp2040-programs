import serial
from time import sleep
from datetime import datetime, timedelta


with serial.Serial('/dev/ttyACM0',
                   baudrate=115200,
                   writeTimeout=0,
                   timeout=10,
                   rtscts=False,
                   dsrdtr=False) as ser:

    totalDiff = timedelta(seconds=0.0)

    for i in range(100):
        startTime = datetime.now()
        ser.write(b'a')
        answer = ser.readline()
        endTime = datetime.now()
        answer = answer.strip()
        if (len(answer) != 100):
            print("Incomplete answer")
        totalDiff += endTime - startTime

    print(f"Average rt time: {totalDiff / 100.0}")

