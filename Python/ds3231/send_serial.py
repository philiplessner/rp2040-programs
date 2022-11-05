import select
import sys
import utime


while True:

    if select.select([sys.stdin],[],[],0)[0]:
        print('Hello, World!')
        utime.sleep(1)

